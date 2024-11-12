from django.db import models

# Create your models here.

class Part(models.Model):
    isim = models.CharField(max_length=100)
    araba_marka = models.ForeignKey('airplanes.Airplane', on_delete=models.CASCADE)  
    stok_adedi = models.PositiveIntegerField()  

    class Meta:
        verbose_name_plural = "Parts"
    
    def __str__(self):
        return f"{self.isim} - {self.araba_marka}"
    