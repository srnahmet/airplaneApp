from django.contrib import admin
from .models import UAV, Part, Team, Employee

# Register your models here.
admin.site.register(UAV)
admin.site.register(Part)
admin.site.register(Team)
admin.site.register(Employee)
