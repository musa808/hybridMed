from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileForm
from .models import Profile


# ================= REGISTER =================


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()

            # Save the profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('accounts:login')
        else:
            # Debugging: print errors
            print(user_form.errors)
            print(profile_form.errors)

    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
# ================= LOGIN =================
import random
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store in session
            request.session['otp'] = str(otp)
            request.session['otp_user_id'] = user.id

            # Send OTP (email)
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                'your@email.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('accounts:verify_otp')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
from django.contrib.auth import login
from django.contrib.auth import get_user_model

User = get_user_model()

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_id = request.session.get('otp_user_id')

        if entered_otp == session_otp:
            user = User.objects.get(id=user_id)
            login(request, user)

            # Clear session
            request.session.pop('otp', None)
            request.session.pop('otp_user_id', None)

            # Role-based redirect
            if user.is_staff:
                return redirect('appointment:admin_dashboard')

            if user.profile.role == "doctor":
                return redirect('doctors:doctor_dashboard')

            if user.profile.role == "patient":
                return redirect('patients:patient_dashboard')

            return redirect('home_view')

        else:
            return render(request, 'accounts/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'accounts/verify_otp.html')
import random
from django.core.mail import send_mail
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store OTP in session
            request.session['otp'] = str(otp)
            request.session['otp_user_id'] = user.id

            # Send email
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('accounts:verify_otp')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('home_view')


# ================= PROFILE =================
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

# views.p



# ---------- Export to PDF ----------
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.timezone import localtime
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from PyPDF2 import PdfReader

from .models import SymptomCheck


# -------------------- Dashboard --------------------
def records_dashboard(request):
    """Show all symptom records and handle imports directly from dashboard."""
    records = SymptomCheck.objects.all().order_by('-created_at')

    # Handle Excel or PDF imports if POST request
    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            _import_excel(request.FILES['excel_file'])
            messages.success(request, "Excel records imported successfully!")
            return redirect('accounts:records_dashboard')

        if 'pdf_file' in request.FILES:
            _import_pdf(request.FILES['pdf_file'])
            messages.success(request, "PDF records imported successfully!")
            return redirect('accounts:records_dashboard')

    return render(request, "accounts/records_dashboard.html", {"records": records})


# -------------------- Helper Functions for Imports --------------------
def _import_excel(excel_file):
    """Helper function to import Excel file."""
    df = pd.read_excel(excel_file, engine='openpyxl')
    for _, row in df.iterrows():
        try:
            user = User.objects.get(username=row['Patient'])
            SymptomCheck.objects.create(
                patient=user,
                symptoms=row['Symptoms'],
                ai_response=row['AI Diagnosis']
            )
        except User.DoesNotExist:
            continue


def _import_pdf(pdf_file):
    """Helper function to import PDF file."""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text = page.extract_text()
        lines = text.splitlines()
        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 4:
                    try:
                        user = User.objects.get(username=parts[0])
                        SymptomCheck.objects.create(
                            patient=user,
                            symptoms=parts[1],
                            ai_response=parts[2]
                        )
                    except User.DoesNotExist:
                        continue


# -------------------- Export PDF --------------------
from django.http import HttpResponse
from django.utils.timezone import localtime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import SymptomCheck


def export_symptoms_pdf(request):
    records = SymptomCheck.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SymptomRecords.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    y = 750  # starting vertical position

    p.drawString(50, y, "Symptom Records")
    y -= 40

    for r in records:
        created = localtime(r.created_at).strftime("%Y-%m-%d %H:%M")

        p.drawString(50, y, f"User: {r.user}")
        y -= 20
        p.drawString(50, y, f"Symptoms: {r.symptoms}")
        y -= 20
        p.drawString(50, y, f"Date: {created}")
        y -= 40

        if y < 50:
            p.showPage()
            y = 750

    p.save()
    return response


# -------------------- Export Excel --------------------
def export_symptoms_excel(request):
    records = SymptomCheck.objects.all().values(
        'patient__username', 'symptoms', 'ai_response', 'created_at'
    )
    df = pd.DataFrame(records)

    # Convert 'created_at' to naive datetime (remove timezone)
    if not df.empty:
        df['created_at'] = df['created_at'].dt.tz_localize(None)

    df.rename(columns={
        'patient__username': 'Patient',
        'symptoms': 'Symptoms',
        'ai_response': 'AI Diagnosis',
        'created_at': 'Date'
    }, inplace=True)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="symptom_records.xlsx"'
    df.to_excel(response, index=False, engine='openpyxl')
    return response


from .models import Payment
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import Payment, Consultation
import stripe


from django.shortcuts import render, get_object_or_404, redirect

from .models import Payment, Consultation, Appointment




def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    consultation = getattr(appointment, 'consultation', None)

    # Prevent duplicate payments
    payment, created = Payment.objects.get_or_create(
        appointment=appointment,
        defaults={
            'user': request.user,
            'consultation': consultation,
            'amount': consultation.fee if consultation else 1000,
            'status': 'pending'
        }
    )

    if request.method == 'POST':
        method = request.POST.get('payment_method')

        # ================= STRIPE =================
        if method == 'stripe':
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Appointment Payment'},
                        'unit_amount': int(payment.amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/payment-success/{payment.id}/'),
                cancel_url=request.build_absolute_uri(f'/payment-cancel/{payment.id}/'),
            )
            return redirect(session.url, code=303)

        # ================= MPESA =================
        elif method == 'mpesa':
            phone_number = request.POST.get('phone_number')

            if not phone_number:
                messages.error(request, 'Phone number is required for Mpesa.')
                return redirect(request.path)

            # TODO: Trigger Mpesa STK Push here
            payment.payment_method = 'mpesa'
            payment.phone_number = phone_number
            payment.status = 'pending'
            payment.save()

            messages.info(request, 'Mpesa STK Push sent to your phone.')
            return redirect(request.path)

        # ================= INSURANCE =================
        elif method == 'insurance':
            provider = request.POST.get('insurance_provider')

            if not provider:
                messages.error(request, 'Insurance provider is required.')
                return redirect(request.path)

            payment.payment_method = 'insurance'
            payment.insurance_provider = provider
            payment.status = 'completed'
            payment.save()

            # Mark appointment as paid
            appointment.is_paid = True
            appointment.save()

            messages.success(request, f'Covered by {provider}.')
            return redirect('accounts:view_receipt', payment.id)

        else:
            messages.error(request, 'Invalid payment method.')
            return redirect(request.path)

    return render(request, 'accounts/payment.html', {
        'payment': payment,
        'appointment': appointment,
        'consultation': consultation,
    })



from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import stripe
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY  # make sure this is set in your settings.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Payment
import stripe

def payment_page(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('payment_method', 'stripe')
        payment.payment_method = method
        payment.save()

        if method == 'stripe':
            # Stripe Checkout
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'Appointment Payment #{payment.id}'},
                        'unit_amount': int(payment.amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/payment-success/{payment.id}/'),
                cancel_url=request.build_absolute_uri(f'/payment-cancel/{payment.id}/'),
            )
            return redirect(session.url, code=303)

        elif method == 'mpesa':
            phone_number = request.POST.get('phone_number')
            if not phone_number:
                messages.error(request, "Phone number is required for M-Pesa.")
                return redirect(request.path)
            # TODO: trigger Mpesa payment API
            messages.success(request, f"M-Pesa payment request sent to {phone_number}.")
            payment.status = 'pending'
            payment.save()
            return redirect(request.path)

        elif method == 'cash':
            payment.status = 'pending'
            payment.save()
            messages.success(request, "Cash payment selected. Pay at the clinic.")
            return redirect(request.path)

        elif method == 'insurance':
            provider = request.POST.get('insurance_provider')
            if not provider:
                messages.error(request, "Insurance provider is required.")
                return redirect(request.path)
            payment.status = 'completed'  # assuming insurance clears instantly
            payment.insurance_provider = provider
            payment.save()
            messages.success(request, f"Payment covered by {provider} insurance.")
            return redirect(request.path)

        else:
            messages.error(request, "Invalid payment method selected.")
            return redirect(request.path)

    return render(request, 'accounts/payment.html', {'payment': payment})
# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Payment

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Payment
from .mpesa import lipa_na_mpesa  # Your M-Pesa utility function

def pay_consultation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    # Prevent double payment
    if payment.status == 'completed':
        messages.info(request, "This consultation is already paid.")
        return redirect('patients:patient_dashboard')

    if request.method == 'POST':
        # ✅ Get selected payment method from the form
        selected_method = request.POST.get('payment_method', 'stripe')
        payment.payment_method = selected_method
        payment.save()

        if selected_method == 'mpesa':
            phone_number = request.POST.get('phone_number')
            if not phone_number:
                messages.error(request, "Please enter your phone number for M-Pesa payment.")
                return render(request, 'accounts/pay_consultation.html', {'payment': payment})

            # Trigger M-Pesa STK Push
            response = lipa_na_mpesa(
                phone_number,
                int(payment.amount),
                f"CONSULT-{payment.id}",
                "Consultation Payment"
            )
            # Save CheckoutRequestID for tracking
            payment.transaction_id = response.get("CheckoutRequestID", "")
            payment.save()

            messages.success(request, "M-Pesa payment initiated. Check your phone to complete.")
            return redirect('patients:patient_dashboard')

        elif selected_method == 'insurance':
            # Payment handled by insurance
            payment.status = 'completed'
            payment.save()
            messages.success(request, "Payment completed via insurance.")
            return redirect('patients:patient_dashboard')

        else:
            # Cash, Stripe, or PayPal – mark as completed immediately for now
            payment.status = 'completed'
            payment.save()
            messages.success(request, "Payment successful!")
            return redirect('patients:patient_dashboard')

    return render(request, 'accounts/pay_consultation.html', {'payment': payment})
from .models import Notification

def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/notifications.html', {'notifications': notifications})

def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('accounts:notifications_list')
from .models import Message
def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'accounts/inbox.html', {'messages': messages_received})

def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(sender=request.user, recipient=recipient, subject=subject, body=body)
        messages.success(request, "Message sent!")
        return redirect('accounts:inbox')
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'accounts/send_message.html', {'users': users})
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import OnlineConsultation

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from consultations.models import Consultation
import uuid


from .utils import create_google_meet_event

def create_consultation_link(request, consultation_id):
    consultation = get_object_or_404(
        Consultation,
        id=consultation_id
    )

    online, created = OnlineConsultation.objects.get_or_create(
        patient=consultation.patient,
        doctor=consultation.doctor
    )

    if not online.link:
        online.link = create_google_meet_event()
        online.save()

    return redirect(online.link)
from openai import OpenAI
from django.conf import settings
from django.shortcuts import render
from .forms import SymptomCheckerForm

# Initialize client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def ai_symptom_checker(request):
    diagnosis = None

    if request.method == 'POST':
        form = SymptomCheckerForm(request.POST)

        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            symptoms = form.cleaned_data['symptoms']

            prompt = f"""
            Patient details:
            Age: {age}
            Gender: {gender}
            Symptoms: {symptoms}

            Provide:
            1. Possible conditions
            2. Severity level (Mild/Moderate/Emergency)
            3. Recommended next steps

            Keep it simple for the patient.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",  # better & cheaper
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical assistant. Do not give final diagnoses. Suggest possibilities and advise seeing a doctor."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5
            )

            diagnosis = response.choices[0].message.content

    else:
        form = SymptomCheckerForm()

    return render(request, "accounts/symptoms_result.html", {
        "form": form,
        "diagnosis": diagnosis
    })
from django.shortcuts import render
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY  # make sure you put your API key in settings

def symptom_checker(request):
    result = None
    if request.method == "POST":
        symptoms = request.POST.get("symptoms")
        if symptoms:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"I have these symptoms: {symptoms}. What could be the possible causes?"}]
            )
            result = response.choices[0].message['content']
    return render(request, "accounts/symptom_form.html", {"result": result})

from django.shortcuts import render, get_object_or_404
from .models import Consultation, OnlineConsultation
from django.contrib.auth.decorators import login_required

@login_required
def consultation_room(request, consultation_id):
    # Get the consultation for the logged-in user
    consultation = get_object_or_404(Consultation, id=consultation_id)

    # Get the online consultation link (if created)
    online_consultation, created = OnlineConsultation.objects.get_or_create(
        consultation=consultation,
        defaults={'link': ''}  # you can generate link if using Google Meet/Zoom
    )

    context = {
        "consultation": consultation,
        "online_link": online_consultation.link,
    }

    return render(request, "accounts/consultation_room.html", context)
from django.utils.translation import gettext as _

def my_view(request):
    message = _("Welcome to Medical System")
    return HttpResponse(message)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Prescription
from consultations.models import Consultation

def create_prescription(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == "POST":
        medicines = request.POST.get("medicines")
        notes = request.POST.get("notes")

        prescription, created = Prescription.objects.get_or_create(
            consultation=consultation,
            defaults={
                "doctor": request.user,
                "patient": consultation.patient,
                "medicines": medicines,
                "notes": notes
            }
        )

        if not created:
            # If it already exists, update instead of crashing
            prescription.medicines = medicines
            prescription.notes = notes
            prescription.save()

            messages.info(request, "Prescription updated successfully.")
        else:
            messages.success(request, "Prescription created successfully.")

        return redirect('doctors:doctor_dashboard')

    return render(request, 'accounts/create_prescription.html', {
        'consultation': consultation
    })
def view_prescription(request, consultation_id):
    try:
        prescription = Prescription.objects.get(
            consultation__id=consultation_id
        )
    except Prescription.DoesNotExist:
        return HttpResponse(
            "No prescription has been created for this consultation yet.",
            status=404
        )

    return render(request, 'accounts/view_prescription.html', {
        'prescription': prescription
    })
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db import transaction
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from .models import Payment, Receipt


# ======================================
# PAYMENT SUCCESS (marks completed + receipt)
# ======================================
@transaction.atomic
def payment_success(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        user=request.user
    )

    # Prevent duplicate processing
    if payment.status != 'completed':
        payment.status = 'completed'
        payment.transaction_id = payment.transaction_id or str(uuid.uuid4())
        payment.save()

    # Ensure receipt exists
    receipt, created = Receipt.objects.get_or_create(
        payment=payment,
        defaults={
            "receipt_number": f"RCPT-{uuid.uuid4().hex[:8].upper()}"
        }
    )

    # Fix missing receipt number
    if not receipt.receipt_number:
        receipt.receipt_number = f"RCPT-{uuid.uuid4().hex[:8].upper()}"
        receipt.save()

    return redirect('accounts:view_receipt', payment_id=payment.id)


# ======================================
# VIEW RECEIPT (HTML PAGE)
# ======================================
import uuid
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Payment, Receipt

import uuid
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Payment, Receipt


@login_required
def view_receipt(request, payment_id):
    # Get payment belonging to the logged-in user
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        user=request.user
    )

    # Block if not completed
    if payment.status != 'completed':
        return HttpResponse(
            "Payment not completed. Please complete payment to view receipt.",
            status=403
        )

    # Get or create receipt
    receipt, created = Receipt.objects.get_or_create(
        payment=payment,
        defaults={
            "receipt_number": f"RCPT-{uuid.uuid4().hex[:8].upper()}",
        }
    )

    context = {
        'receipt': receipt,
        'payment': payment,  # ✅ include payment
        'hospital_name': "Umma University Clinic",
        'signature_url': "/static/images/signature.png",
        'stamp_url': "/static/images/stamp.png",
    }

    return render(request, 'accounts/receipt.html', context)
# ======================================
# DOWNLOAD RECEIPT (PDF)
# ======================================
import uuid
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


def download_receipt(request, payment_id):
    # Get payment belonging to the logged-in user
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        user=request.user
    )

    # Block if not completed
    if payment.status != 'completed':
        return HttpResponse("Payment not completed", status=403)

    # Get or create receipt
    receipt, created = Receipt.objects.get_or_create(
        payment=payment,
        defaults={
            "receipt_number": f"RCPT-{uuid.uuid4().hex[:10].upper()}"
        }
    )

    # ===== GENERATE PDF =====
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="receipt_{receipt.receipt_number}.pdf"'
    )

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # ===== HOSPITAL HEADER =====
    elements.append(Paragraph("Umma University Clinic", styles['Title']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("MEDICAL RECEIPT", styles['Heading2']))
    elements.append(Spacer(1, 20))

    # ===== RECEIPT DETAILS =====
    elements.append(Paragraph(f"Receipt No: {receipt.receipt_number}", styles['Normal']))
    elements.append(Paragraph(f"Transaction ID: {payment.transaction_id}", styles['Normal']))
    elements.append(Paragraph(f"Patient: {payment.user}", styles['Normal']))
    elements.append(Paragraph(f"Amount Paid: KES {payment.amount}", styles['Normal']))
    elements.append(Paragraph(f"Payment Method: {payment.payment_method}", styles['Normal']))

    # Safe date handling
    date_issued = (
        receipt.issued_at.strftime('%Y-%m-%d %H:%M')
        if receipt.issued_at else "N/A"
    )
    elements.append(Paragraph(f"Date: {date_issued}", styles['Normal']))

    elements.append(Spacer(1, 30))

    # ===== SIGNATURE & STAMP =====
    signature_path = os.path.join(settings.BASE_DIR, "static/images/signature.png")
    stamp_path = os.path.join(settings.BASE_DIR, "static/images/stamp.png")

    # Signature
    if os.path.exists(signature_path):
        elements.append(Paragraph("Authorized Signature:", styles['Normal']))
        elements.append(Spacer(1, 5))
        elements.append(Image(signature_path, width=120, height=60))

    elements.append(Spacer(1, 20))

    # Stamp
    if os.path.exists(stamp_path):
        elements.append(Paragraph("Official Stamp:", styles['Normal']))
        elements.append(Spacer(1, 5))
        elements.append(Image(stamp_path, width=120, height=120))

    elements.append(Spacer(1, 25))

    # Footer
    elements.append(Paragraph("Thank you for your payment.", styles['Italic']))

    # Build PDF
    doc.build(elements)

    return response