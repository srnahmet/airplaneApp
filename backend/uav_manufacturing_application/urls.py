from django.urls import include, path
from rest_framework.routers import DefaultRouter
from uav_manufacturing_application import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'uav', views.UAVViewSet)
router.register(r'parts', views.PartViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'employee', views.EmployeeViewSet)

urlpatterns = [
    # genel api lar
    path('', include(router.urls)),
    # tipler
    path('part-types/', views.PartTypeViewSet.as_view(), name='part-type-list'), 
    path('uav-types/', views.UAVTypeViewSet.as_view(), name='uav-types-list'),
    # datatables api ları
    path('uav-list/', views.UAVListView.as_view(), name='uav-list'), 
    path('parts-list/', views.PartListView.as_view(), name='parts-list'), 
    path('teams-list/', views.TeamListView.as_view(), name='teams-list'), 
    path('employee-list/', views.EmployeeListView.as_view(), name='employee-list'), 
    path('employees/<int:team_id>/', views.EmployeeListViewByTeamId.as_view(), name='employee-list'),
    #token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('custom-token/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
]
