from django.db import models
from django.contrib.auth.models import User


# İHA Modeli
class UAV(models.Model):
    name = models.CharField(max_length=50,default=None)
    model = models.CharField(max_length=100,default=None)

    def __str__(self):
        return self.name

# İHA Modeli: İHA tipini tanımlar
class UAVType(models.Model):
    name = models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.name

# PartType Modeli: Parça türünü tanımlar
class PartType(models.Model):
    name = models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.name

# Part Modeli
class Part(models.Model):
    name = models.CharField(max_length=50,default=None)
    uav_type = models.ForeignKey(UAVType, on_delete=models.CASCADE,default=None)  # Parçanın ait olduğu iha tipi
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE,default=None)  # Parçanın türü 
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE,default=None)  # Part yalnızca bir UAV ile ilişkili

    def __str__(self):
        return f"{self.name} ({self.part_type.name} - {self.uav_type.name})"

# Team Modeli
class Team(models.Model):
    name = models.CharField(max_length=100,default=None)
    is_montage_team = models.BooleanField(default=False) # Takım montaj takımı mı?
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE, null=True, blank=True)  # Her takım yalnızca belirli bir türde parça üretir, montaj takımı için belirtilmez

    def __str__(self):
        return self.name

# Employee Modeli.name
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='employee', null=True) # Her çalışan bir takıma atanabilir

    def __str__(self):
        return self.name
