from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AppointmentForm


@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment/appointment_list.html', {'appointment': appointments})


@login_required
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('appointment:appointment_list')
    return render(request, 'appointment/appointment_form.html', {'form': form})


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        return redirect('appointment:appointment_list')
    return render(request, 'appointment/appointment_form.html', {'form': form})


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('appointment:appointment_list')

from patients.models import Patient
from doctors.models import Doctor
from appointment.models import Appointment
from records.models import MedicalRecord
from consultations.models import Consultation

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'patients_count': Patient.objects.count(),
        'doctors_count': Doctor.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'records_count': MedicalRecord.objects.count(),
        'consultations_count': Consultation.objects.count(),
    }
    return render(request, 'appointment/admin_dashboard.html', context)