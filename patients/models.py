from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True)
    age=models.IntegerField()
    medical_history=models.TextField()
    

    def __str__(self):
        return self.name
