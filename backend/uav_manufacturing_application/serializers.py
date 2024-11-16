from rest_framework import serializers
from .models import UAV, Part, Team, Employee, UAVType, PartType

class DatatableParamsSerializer(serializers.Serializer):
    start = serializers.IntegerField(default=0)
    length = serializers.IntegerField(default=10)
    search_value = serializers.CharField(default='', required=False)
    order_column = serializers.CharField(default='id')
    order_dir = serializers.ChoiceField(choices=['asc', 'desc'], default='asc')


class PartTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartType
        fields = ['id', 'name']

class UAVTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAVType
        fields = ['id', 'name']

class UAVSerializer(serializers.ModelSerializer):
    uav_type = UAVTypeSerializer()
    class Meta:
        model = UAV
        fields = ['id', 'create_date', 'uav_type']

class PartSerializer(serializers.ModelSerializer):
    uav_type_name = UAVTypeSerializer(source='uav_type', read_only=True)
    part_type_name = PartTypeSerializer(source='part_type', read_only=True)
    uav_name = UAVSerializer(source='uav', read_only=True)

    class Meta:
        model = Part
        fields = ['id', 'name', 'uav_type', 'uav_type_name', 'part_type', 'part_type_name', 'uav', 'uav_name']

class TeamSerializer(serializers.ModelSerializer):
    part_type_name = PartTypeSerializer(source='part_type', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'part_type', 'part_type_name']

class EmployeeSerializer(serializers.ModelSerializer):
    team_name = TeamSerializer(source='team', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'team', 'team_name']
