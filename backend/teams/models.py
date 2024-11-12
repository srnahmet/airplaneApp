from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100) 
    connected_part = models.ForeignKey('parts.Part', on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.name
    

class Employee(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="employees") 

    def __str__(self):
        return f"{self.name} - {self.team.name}"