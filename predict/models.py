from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=50)
    age = models. IntegerField()
    gender = models.CharField(max_length=30)
    height = models. IntegerField()
    weight = models. IntegerField()
    symptom1 = models.CharField(max_length=30)
    symptom2 = models.CharField(max_length=30, blank=True)
    symptom3 = models.CharField(max_length=30, blank=True)
    symptom4 = models.CharField(max_length=30, blank=True)
    symptom5 = models.CharField(max_length=30, blank=True)
    disease = models.CharField(max_length=30)
    consultDoctor = models.CharField(max_length=30)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)


    def __str__(self):
        return self.name
