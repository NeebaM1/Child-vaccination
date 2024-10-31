from django.contrib import admin
from vaccination.models import  Userdetail,Vaccinations,TimePeriod

# Register your models here.
admin.site.register(Userdetail)
admin.site.register(Vaccinations)
admin.site.register(TimePeriod)
