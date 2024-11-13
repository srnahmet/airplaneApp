from rest_framework import serializers
from .models import Airplane, Part, Team, Employee

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
