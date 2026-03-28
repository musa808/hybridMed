from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date=models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(null=True)
    status = models.CharField(max_length=20, default='pending')
    
    # ✅ Add this field
    fee = models.DecimalField(max_digits=6, decimal_places=2, default=10)  # default $50