from django.db import models

# Create your models here.
class Airplane(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Part(models.Model):
    name = models.CharField(max_length=50)
    airplane = models.ForeignKey(Airplane, related_name='parts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name