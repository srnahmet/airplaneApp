from django.shortcuts import render
from rest_framework import viewsets
from .models import Airplane, Part, Team, Employee
from .serializers import AirplaneSerializer, PartSerializer, TeamSerializer, EmployeeSerializer

# Create your views here.

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer