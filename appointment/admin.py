from django.contrib import admin
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'status'
    )

    list_filter = (
        'status',
        'appointment_date'
    )

    search_fields = (
        'patient__username',
        'doctor__username'
    )

    ordering = ('-appointment_date',)


admin.site.register(Appointment, AppointmentAdmin)