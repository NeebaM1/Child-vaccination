from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userdetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    choice_field=models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class TimePeriod(models.Model):
    timeperiod_name = models.CharField(max_length=50)
    timeperiod_indays=models.IntegerField(null=True)

    def __str__(self):
        return self.timeperiod_name


class Vaccinations(models.Model):

    time_period=models.ForeignKey(TimePeriod,on_delete=models.CASCADE,null=True)
    vaccine=models.CharField(max_length=100)


    def __str__(self):
        return self.vaccine



