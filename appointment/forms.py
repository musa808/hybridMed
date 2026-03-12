from django import forms
from django.contrib.auth.models import User
from .models import Appointment
from accounts.models import Profile


class AppointmentForm(forms.ModelForm):

    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Appointment
        fields = [
            'patient',
            'doctor',
            'appointment_date',
            'appointment_time',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        doctor_ids = Profile.objects.filter(role='doctor').values_list('user_id', flat=True)
        patient_ids = Profile.objects.filter(role='patient').values_list('user_id', flat=True)

        self.fields['doctor'].queryset = User.objects.filter(id__in=doctor_ids)
        self.fields['patient'].queryset = User.objects.filter(id__in=patient_ids)