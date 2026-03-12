from django import forms
from .models import Patient
from django.contrib.auth.models import User
from accounts.models import Profile

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter only users with patient role
        patient_ids = Profile.objects.filter(role='patient').values_list('user_id', flat=True)
        self.fields['user'].queryset = User.objects.filter(id__in=patient_ids)

        # Optional: If your Patient model has a doctor field, filter only doctors
        if 'doctor' in self.fields:
            doctor_ids = Profile.objects.filter(role='doctor').values_list('user_id', flat=True)
            self.fields['doctor'].queryset = User.objects.filter(id__in=doctor_ids)