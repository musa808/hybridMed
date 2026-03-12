
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

def patient_dashboard(request):

    appointments = Appointment.objects.filter(patient=request.user)
    consultations = Consultation.objects.filter(patient=request.user)
    records = MedicalRecord.objects.filter(patient=request.user)

    context = {
        'appointments': appointments,
        'consultations': consultations,
        'records': records
    }

    return render(request, 'patients/patient_dashboard.html', context)
