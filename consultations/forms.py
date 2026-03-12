from django import forms
from .models import Consultation
from django.contrib.auth.models import User
from accounts.models import Profile


class ConsultationForm(forms.ModelForm):

    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = Consultation
        fields = [
            'patient',
            'doctor',
            'consultation_type',
            'appointment_date',
            'appointment_time',
            'symptoms'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter users based on profile roles
        doctor_ids = Profile.objects.filter(role='doctor').values_list('user_id', flat=True)
        patient_ids = Profile.objects.filter(role='patient').values_list('user_id', flat=True)

        self.fields['doctor'].queryset = User.objects.filter(id__in=doctor_ids)
        self.fields['patient'].queryset = User.objects.filter(id__in=patient_ids)