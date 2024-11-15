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

import os
# Create your views here.

# mainpage
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
#

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

# Tüm model view'larında Datatables işlemlerini yapmak için temel sınıf 
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
        order_column = datatable_params.validated_data['order_column']
        order_dir = datatable_params.validated_data['order_dir']

        # Sıralama işlemi
        order_by_columns = ['id', 'name']  # Bu, her model için özelleştirilebilir
        order_by = order_by_columns[int(order_column)]
        if order_dir == 'desc':
            order_by = '-' + order_by

        # Arama işlemi
        queryset = self.model.objects.all()
        if search_value:
            queryset = queryset.filter(Q(name__icontains=search_value))

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

class TeamListView(BaseListView):
    model = Team
    serializer_class = TeamSerializer
    # def get(self, request, *args, **kwargs):
    #     teams = Team.objects.prefetch_related('part_type').all()  # Takımlarla ilişkili parça türlerini çekiyoruz
    #     serializer = TeamSerializer(teams, many=True)
    #     return Response(serializer.data)

class EmployeeListView(BaseListView):
    model = Employee
    serializer_class = EmployeeSerializer
    # def get(self, request, *args, **kwargs):
    #     employees = Employee.objects.select_related('team').all()  # Çalışanlarla ilişkili takımları çekiyoruz
    #     serializer = EmployeeSerializer(employees, many=True)
    #     return Response(serializer.data)

class UAVTypeViewSet(generics.ListAPIView):
    queryset = UAVType.objects.all()
    serializer_class = UAVTypeSerializer

class PartTypeViewSet(generics.ListAPIView):
    queryset = PartType.objects.all()
    serializer_class = PartTypeSerializer
#endregion