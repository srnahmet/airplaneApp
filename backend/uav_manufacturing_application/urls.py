from django.urls import include, path
from rest_framework.routers import DefaultRouter
from uav_manufacturing_application import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
# router.register(r'uav', views.UAVViewSet)
# router.register(r'parts', views.PartViewSet)
# router.register(r'teams', views.TeamViewSet)
router.register(r'employee', views.EmployeeViewSet)

urlpatterns = [
    # genel api lar
    path('', include(router.urls)),
    path('parts/', views.PartAPIView.as_view(), name='part-create'),
    path('parts-by-id/<int:id>/', views.PartAPIView.as_view(), name='part-delete'),
    # tipler
    path('part-types/', views.PartTypeViewSet.as_view(), name='part-type-list'), 
    path('uav-types/', views.UAVTypeViewSet.as_view(), name='uav-types-list'),
    # datatables api ları
    path('uav-list/', views.UAVListView.as_view(), name='uav-list'), 
    path('teams-list/', views.TeamListView.as_view(), name='teams-list'), 
    path('employee-list/', views.EmployeeListView.as_view(), name='employee-list'), 
    # by-id list
    path('employees/<int:team_id>/', views.EmployeeListViewByTeamId.as_view(), name='employee-list-by-team-id'),
    path('parts-by-team-id/', views.PartListViewByTeamId.as_view(), name='uavs-by-team'),
    path('parts-list-by-uav-id/<int:uav_id>/', views.PartListViewByUAVId.as_view(), name='part-list-by-uav-id'),
    path('parts-list-by-uav-type-id/<int:uav_type_id>/', views.PartListViewByUavTypeId.as_view(), name='part-list-by-uav-type-id'),
    path('parts-list-by-uav-type-id-count/<int:uav_type_id>/', views.PartListViewByUavTypeIdPartTypeCounts.as_view(), name='part-list-by-uav-type-id'),

    # montaj
    path('create-uav/', views.CreateUAVAndAssignParts.as_view(), name='create_uav'),

    #token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('custom-token/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
]
