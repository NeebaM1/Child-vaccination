from django.db import models

# Create your models here.

class Hospital_Detail(models.Model):
    hs_name=models.CharField(max_length=60)
    hs_place=models.CharField(max_length=30)


    def __str__(self):
        return self.hs_name
