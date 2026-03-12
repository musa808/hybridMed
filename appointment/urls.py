from django.urls import path
from . import views
app_name='appointment'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard')
]