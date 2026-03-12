from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Consultation
from .forms import ConsultationForm


@login_required
def consultation_list(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultations/consultation_list.html', {'consultations': consultations})


@login_required
def consultation_create(request):
    form = ConsultationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('consultations:consultation_list')
    return render(request, 'consultations/consultation_form.html', {'form': form})


@login_required
def consultation_update(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    form = ConsultationForm(request.POST or None, instance=consultation)
    if form.is_valid():
        form.save()
        return redirect('consultations:consultation_list')
    return render(request, 'consultations/consultation_form.html', {'form': form})


@login_required
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return redirect('consultations:consultation_list')