from django.db import models
from django.contrib.auth.models import User
class Appointment(models.Model):
    STATUS=(
        ('pending','Pending'),
        ('approved','Approved'),
        ('completed','Completed'),
    )
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='patients_appointments')
    doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor_appointments')
    appointment_date=models.DateField()
    appointment_time=models.TimeField()
    status=models.CharField(max_length=20,choices=STATUS,default='pending')
    
