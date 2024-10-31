from django.db import models
from vaccination.models import Vaccinations,Userdetail,TimePeriod
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Child_Details(models.Model):
    parent=models.ForeignKey(Userdetail,on_delete=models.CASCADE,null=True)
    child_name=models.CharField(max_length=20)
    child_age=models.CharField(max_length=100)
    child_address=models.TextField()
    child_dob=models.DateField()
    child_father_name=models.CharField(max_length=20)
    child_mother_name=models.CharField(max_length=20)
    child_ph=models.BigIntegerField()






    def __str__(self):
        return self.child_name

class Child_vaccine(models.Model):

    vaccine=models.ForeignKey(Vaccinations,on_delete=models.CASCADE)
    child=models.ForeignKey(Child_Details,on_delete=models.CASCADE)
    expected_date=models.CharField(null=True,max_length=100)
    vaccine_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.child.child_name} {self.vaccine.time_period.timeperiod_indays}"
    

class Book_Appoinment(models.Model):
    child=models.ForeignKey(Child_Details,on_delete=models.CASCADE)  
    vaccine=models.ForeignKey(Vaccinations,on_delete=models.CASCADE) 
    appoinment_date=models.DateField()
    


    def __str__(self):
        return  f"{self.child.child_name} {self.appoinment_date}"
    

class appoinment_table(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    child=models.ForeignKey(Child_Details,on_delete=models.CASCADE)  
    vaccine=models.ForeignKey(Vaccinations,on_delete=models.CASCADE)
    appoinment_date=models.DateField()
    appoinment_status=models.CharField(default="pending",max_length=30)


    def __str__(self):
        return f"{self.child.child_name} {self.appoinment_status}"
        


