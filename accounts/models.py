from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('doctor','Doctor'),
        ('patient','Patient'),
        
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} Profile"
    
# models.py



class SymptomCheck(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check by {self.patient.username} on {self.created_at}"

from django.db import models
from django.contrib.auth.models import User
from appointment.models import Appointment

from django.contrib.auth.models import User
from django.db import models
from appointment.models import Appointment
from consultations.models import Consultation

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('insurance', 'Insurance'),
        ('mpesa', 'Mpesa'),
        ('stripe', 'Stripe'),
        
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='payment',
        null=True,
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)

    # 🔹 New fields for insurance
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)  # e.g., SHA
    insurance_number = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class Insurance(models.Model):
    name = models.CharField(max_length=100)  # e.g SHA
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username} : {self.subject}"
    
import uuid


class OnlineConsultation(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    link = models.URLField(blank=True, null=True)
    scheduled_at = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.conf import settings
from consultations.models import Consultation

class Prescription(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_prescriptions')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_prescriptions')

    medicines = models.TextField(blank=True,null=True)  
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient}"
    
class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=100, unique=True)

    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_number