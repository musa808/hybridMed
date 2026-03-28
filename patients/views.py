
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm
from appointment.models import Appointment
from consultations.models import Consultation
from records.models import MedicalRecord


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('patients:patient_list')
    return render(request, 'patients/patient_form.html', {'form': form})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_detail.html', {'patient': patient})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patients:patient_list')
    return render(request, 'patients/patient_form.html', {'form': form})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patients:patient_list')

from django.shortcuts import render
from accounts.models import Payment # Make sure Payment is imported

def patient_dashboard(request):
    patient = request.user

    # Existing queries
    appointments = Appointment.objects.filter(patient=patient)
    consultations = Consultation.objects.filter(patient=patient)
    records = MedicalRecord.objects.filter(patient=patient)

    # Add payments
    payments = Payment.objects.filter(user=patient).order_by('-created_at')  # latest first

    context = {
        'appointments': appointments,
        'consultations': consultations,
        'records': records,
        'payments': payments,  # new addition
    }

    return render(request, 'patients/patient_dashboard.html', context)