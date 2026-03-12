from django.db import models
from django.contrib.auth.models import User
from consultations.models import Consultation


class MedicalRecord(models.Model):

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    diagnosis = models.TextField()
    treatment = models.TextField()

    prescription = models.TextField(
        blank=True,
        null=True
    )

    lab_report = models.FileField(
        upload_to='lab_reports/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient.username} - {self.created_at.date()}"
