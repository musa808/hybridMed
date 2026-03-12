from django import forms
from .models import MedicalRecord
from django.contrib.auth.models import User
from accounts.models import Profile

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'patient',
            'diagnosis',
            'treatment',
            'prescription',
            'lab_report'
        ]
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter patient dropdown to only users with patient role
        patient_ids = Profile.objects.filter(role='patient').values_list('user_id', flat=True)
        self.fields['patient'].queryset = User.objects.filter(id__in=patient_ids)