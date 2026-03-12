from django.contrib import admin
from .models import Consultation


class ConsultationAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'doctor',
        'consultation_type',
        'appointment_date',
        'appointment_time',
        'status'
    )

    list_filter = (
        'consultation_type',
        'status',
        'appointment_date'
    )

    search_fields = (
        'patient__username',
        'doctor__username',
        'symptoms'
    )


admin.site.register(Consultation, ConsultationAdmin)