from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('prescription/create/<int:consultation_id>/', views.create_prescription, name='create_prescription'),
    path('prescription/view/<int:consultation_id>/', views.view_prescription, name='view_prescription'),
    path('receipt/download/<int:payment_id>/', views.download_receipt, name='download_receipt'),
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('receipt/<int:payment_id>/', views.view_receipt, name='view_receipt'),

    # Export
    path('export/excel/', views.export_symptoms_excel, name='export_symptoms_excel'),
    path('export/pdf/', views.export_symptoms_pdf, name='export_symptoms_pdf'),

    # Payments
    path('make-payment/', views.make_payment, name='make_payment'),
    path('payment/<int:payment_id>/', views.payment_page, name='payment_page'),
    path('pay-consultation/<int:payment_id>/', views.pay_consultation, name='pay_consultation'),

    # Notifications & messaging
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='notification_read'),
    path('inbox/', views.inbox, name='inbox'),
    path('send-message/', views.send_message, name='send_message'),

    # Dashboard & consultations
    path('dashboard/', views.records_dashboard, name='records_dashboard'),
    path('create-consultation/<int:consultation_id>/', views.create_consultation_link, name='create_consultation_link'),
    path('consultation/<uuid:token>/', views.consultation_room, name='consultation_room'),

    # Symptom checker
    path('symptom-checker/', views.ai_symptom_checker, name='ai_symptom_checker'),
]