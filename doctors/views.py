from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor
from .forms import DoctorForm


@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})


@login_required
def doctor_create(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('doctors:doctor_list')
    return render(request, 'doctors/doctor_form.html', {'form': form})


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST or None, instance=doctor)
    if form.is_valid():
        form.save()
        return redirect('doctors:doctor_list')
    return render(request, 'doctors/doctor_form.html', {'form': form})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    return redirect('doctors:doctor_list')

# accounts/views.py or dashboard/views.py


from appointment.models import Appointment
from consultations.models import Consultation
from django.utils import timezone

@login_required
def doctor_dashboard(request):
    doctor = request.user

    # All appointments for this doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    # Count of unique patients
    patient_count = appointments.values('patient').distinct().count()

    # Count of appointments
    appointment_count = appointments.count()

    # Count of consultations
    consultation_count = Consultation.objects.filter(doctor=doctor).count()

    # Upcoming appointments
    today = timezone.now().date()
    upcoming_appointments = appointments.filter(
        appointment_date__gte=today
    ).order_by('appointment_date', 'appointment_time')

    # Recent consultations (latest 5)
    recent_consultations = Consultation.objects.filter(
        doctor=doctor
    ).order_by('-created_at')[:5]

    context = {
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'consultation_count': consultation_count,
        'upcoming_appointments': upcoming_appointments,
        'recent_consultations': recent_consultations,
    }

    return render(request, 'doctors/doctor_dashboard.html', context)