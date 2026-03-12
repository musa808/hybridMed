from django import forms
from .models import Doctor
from django.contrib.auth.models import User
from accounts.models import Profile

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter only users with doctor role
        doctor_ids = Profile.objects.filter(role='doctor').values_list('user_id', flat=True)
        self.fields['user'].queryset = User.objects.filter(id__in=doctor_ids)