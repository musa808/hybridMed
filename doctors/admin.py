from django.contrib import admin
from .models import Doctor


class DoctorAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'specialization',
        'experience_year'
    )

    list_filter = (
        'specialization',
    )

    search_fields = (
        'user__username',
        'specialization'
    )


admin.site.register(Doctor, DoctorAdmin)