from django.contrib import admin
from parent.models import  Child_Details,Child_vaccine,Book_Appoinment,appoinment_table

# Register your models here.
admin.site.register(Child_Details)
admin.site.register(Child_vaccine)
admin.site.register(Book_Appoinment)
admin.site.register(appoinment_table)
