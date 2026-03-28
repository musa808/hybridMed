from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'doctor',
        'appointment_date',  # corrected
        'appointment_time',  # corrected
        'status'
    )

    list_filter = (
        'status',
        'appointment_date'  # corrected
    )

    search_fields = (
        'patient__username',
        'doctor__username'
    )

    ordering = ('-appointment_date',)  # corrected

admin.site.register(Appointment, AppointmentAdmin)