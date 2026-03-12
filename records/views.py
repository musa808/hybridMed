from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .forms import MedicalRecordForm


@login_required
def record_list(request):
    records = MedicalRecord.objects.all()
    return render(request, 'records/record_list.html', {'records': records})


@login_required
def record_create(request):
    form = MedicalRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('records:record_list')
    return render(request, 'records/record_form.html', {'form': form})


@login_required
def record_update(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    form = MedicalRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('records:record_list')
    return render(request, 'records/record_form.html', {'form': form})


@login_required
def record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    record.delete()
    return redirect('records:record_list')