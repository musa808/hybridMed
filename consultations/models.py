from django.db import models
from django.contrib.auth.models import User


# consultations/models.py


class Consultation(models.Model):
    CONSULTATION_TYPE = (
        ('online', 'Online'),
        ('physical', 'Physical Visit'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patient_consultations'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_consultations'
    )

    consultation_type = models.CharField(
        max_length=20,
        choices=CONSULTATION_TYPE
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    symptoms = models.TextField()

    meeting_link = models.URLField(
        blank=True,
        null=True
    )  # Only for online consultations

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Set the consultation fee"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username} ({self.status})"
# consultations/models.py
from django.db import models
from appointment.models import Appointment
from doctors.models import Doctor
from patients.models import Patient

class ConsultationFee(models.Model):
    consultation = models.ForeignKey('Consultation', on_delete=models.CASCADE)  # link to consultation
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fee for {self.consultation} - {self.amount} ({self.status})"
