from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Consultation
from .forms import ConsultationForm


@login_required
def consultation_list(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultations/consultation_list.html', {'consultations': consultations})



# consultations/views.py
from django.shortcuts import redirect
from .models import Consultation, ConsultationFee
from django.contrib.auth.models import User
# consultations/views.py
from django.shortcuts import render, redirect
from .models import Consultation
from .forms import ConsultationForm
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConsultationForm
from .models import Consultation
from accounts.models import Payment


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ConsultationForm
from .models import Consultation
import uuid

@login_required
def consultation_create(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)

        if form.is_valid():
            consultation = form.save(commit=False)

            # Attach logged-in user as patient
            consultation.patient = request.user

            # Set fee based on consultation type
            if consultation.consultation_type == 'online':
                consultation.fee = 1000
                # ✅ Generate system link automatically
                token = str(uuid.uuid4())
                consultation.link = f"https://yourdomain.com/consultation/join/{token}/"
            elif consultation.consultation_type == 'physical':
                consultation.fee = 500

            consultation.save()

            # Get payment method
            payment_method = request.POST.get('payment_method', 'cash')
            insurance_provider = request.POST.get('insurance_provider', None)
            insurance_number = request.POST.get('insurance_number', None)

            # Create payment
            payment = Payment.objects.create(
                consultation=consultation,
                amount=0 if payment_method == 'insurance' else consultation.fee,
                user=request.user,
                status="pending",
                payment_method=payment_method,
                insurance_provider=insurance_provider,
                insurance_number=insurance_number
            )

            messages.success(request, 'Consultation booked. Please complete payment.')

            # Redirect to payment page
            return redirect('accounts:pay_consultation', payment.id)

    else:
        form = ConsultationForm()

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
# consultations/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Consultation
from accounts.models import Payment

def complete_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Only the doctor can mark completed
    if request.user != consultation.doctor:
        messages.error(request, "You cannot complete this consultation.")
        return redirect('consultations:consultation_list')

    consultation.status = 'completed'
    consultation.save()

    # Create payment record if not already created
    if not hasattr(consultation, 'payment'):
     payment = Payment.objects.create(
    consultation=consultation,
    amount=500,
    status="pending"   # ✅ correct field
)
    messages.success(request, "Consultation completed. Payment record created.")
    return redirect('consultations:detail', consultation_id=consultation.id)