from django.contrib import admin
from .models import MedicalRecord

class MedicalRecordAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'doctor',
        'consultation',
        'created_at'
    )

    list_filter = (
        'created_at',
        'doctor',
    )

    search_fields = (
        'patient__username',
        'doctor__username',
        'diagnosis',
    )

    ordering = ('-created_at',)


admin.site.register(MedicalRecord, MedicalRecordAdmin)