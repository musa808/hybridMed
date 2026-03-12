from django.contrib import admin
from .models import Patient


class PatientAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'age',
        'medical_history'
    )

    search_fields = (
        'user__username',
    )


admin.site.register(Patient, PatientAdmin)