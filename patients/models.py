from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True)
    age=models.IntegerField()
    medical_history=models.TextField()
    insurance = models.ForeignKey(
        'accounts.Insurance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    insurance_number = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return self.name
