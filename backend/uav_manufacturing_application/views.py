# from django.shortcuts import render
from .models import UAV, Part, Team, Employee, UAVType,PartType
from .serializers import UAVSerializer, PartSerializer, TeamSerializer, EmployeeSerializer, UAVTypeSerializer,PartTypeSerializer, DatatableParamsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status,viewsets,generics
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import markdown
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count
import os
# Create your views here.

#region token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Token içine ek bilgi ekleyebilirsiniz
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Kullanıcıya ait employee bilgilerini ekleyin
        try:
            employee = Employee.objects.get(user_id=self.user.id)
            team = Team.objects.get(id=employee.team_id)

            data['employee'] = {
                'id': employee.id,
                'name': employee.name,
                'team_id': employee.team_id,  
            }
            data['team'] = {
                'id': team.id,
                'name': team.name,
                'part_type_name': team.part_type.name if team.part_type else None,
                'part_type_id': team.part_type.id if team.part_type else None,
                'is_montage_team':team.is_montage_team  
            }

        except Team.DoesNotExist:
            data['team'] = None
            data['employee'] = {
                'id': employee.id,
                'name': employee.name,
                'team_id': employee.team_id,  
            }
            
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
#endregion

#region mainpage readme
def readme_view(request):
    app_dir = os.path.dirname(os.path.abspath(__file__))  
    readme_path = os.path.join(app_dir, "README.md")
    try:
        with open(readme_path, "r", encoding="utf-8") as file:
            content = file.read()
        # Markdown'u HTML'e dönüştür
        html_content = markdown.markdown(content)
        return HttpResponse(mark_safe(html_content))
    except FileNotFoundError:
        return HttpResponse("README.md dosyası bulunamadı.", status=404)
#endregion

#region Temel Viewlar
class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
#endregion

#region Tüm model view'larında Datatables işlemlerini yapmak için temel sınıf 
class BaseListView(APIView):
    model = None
    serializer_class = None

    @swagger_auto_schema(
        request_body=DatatableParamsSerializer,
        responses={status.HTTP_200_OK: None}
    )
    def post(self, request, *args, **kwargs):
        # Datatables parametreleri
        datatable_params = DatatableParamsSerializer(data=request.data)
        if not datatable_params.is_valid():
            return Response(datatable_params.errors, status=status.HTTP_400_BAD_REQUEST)

        start = datatable_params.validated_data['start']
        length = datatable_params.validated_data['length']
        search_value = datatable_params.validated_data['search_value']
        order_column = datatable_params.validated_data['order_column']  # string değer
        order_dir = datatable_params.validated_data['order_dir']

        # valid_columns = ['id', 'name', 'create_date', 'related_model__title']  
        # if order_column not in valid_columns:
        #     return Response({"error": f"Invalid order column: {order_column}"}, status=status.HTTP_400_BAD_REQUEST)

        order_by = order_column
        if order_dir == 'desc':
            order_by = '-' + order_by

         # Dinamik arama işlemi (özelleştirilebilir)
        queryset = self.model.objects.all()
        if search_value:
            query_filter = Q()
            
            # Modelin tüm alanlarını al ve arama filtresini oluştur
            for field in self.model._meta.get_fields():
                field_name = field.name

                # Eğer ilişkilendirilmiş bir modelse (ForeignKey, OneToOneField vb.)
                if field.is_relation:
                    # İlişkili modelin adını almak için:
                    related_model = field.related_model
                    
                    # İlişkili modeldeki 'name' gibi bir alanda arama yap
                    print("related_model",related_model)
                    if hasattr(related_model, 'name'):  # İlişkili modelin 'name' alanı varsa
                        query_filter |= Q(**{f"{field_name}__name__icontains": search_value})

                else:
                    # İlişkili olmayan alanda (örneğin: 'create_date', 'id') arama yapılır
                    query_filter |= Q(**{f"{field_name}__icontains": search_value})
            
            queryset = queryset.filter(query_filter)

        # Sayfalama ve sıralama
        total_count = self.model.objects.count()
        filtered_count = queryset.count()
        queryset = queryset.order_by(order_by)[start:start + length]
        serializer = self.serializer_class(queryset, many=True)

        response_data = {
            "draw": request.data.get('draw', 0),
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": serializer.data
        }

        return Response(response_data)
#endregion

#region datatables view'ları

# UAVListView
class UAVListView(BaseListView):
    model = UAV
    serializer_class = UAVSerializer

class PartListView(BaseListView):
    model = Part
    serializer_class = PartSerializer
    # def get(self, request, *args, **kwargs):
    #     parts = Part.objects.select_related('uav_type', 'part_type', 'uav').all()  # Parçalarla ilişkili iha türleri, parça türleri ve ihalar
    #     serializer = PartSerializer(parts, many=True)
    #     return Response(serializer.data)

class TeamListView(APIView):
    def get(self, request, *args, **kwargs):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EmployeeListView(BaseListView):
    model = Employee
    serializer_class = EmployeeSerializer

class EmployeeListViewByTeamId(APIView):
    def get(self, request, team_id, *args, **kwargs):
        employees = Employee.objects.filter(team_id=team_id)
        
        if not employees.exists():
            return Response({"detail": "Bu takımın personeli yoktur."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UAVTypeViewSet(generics.ListAPIView):
    queryset = UAVType.objects.all()
    serializer_class = UAVTypeSerializer

class PartTypeViewSet(generics.ListAPIView):
    queryset = PartType.objects.all()
    serializer_class = PartTypeSerializer
#endregion