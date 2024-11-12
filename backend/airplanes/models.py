from django.db import models

# Create your models here.

class Airplane(models.Model):
    isim = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.isim