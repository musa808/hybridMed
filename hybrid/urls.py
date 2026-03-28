from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home_view"),
    path('about/', views.about_view, name="about_view"),

    # Your app URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('consultations/', include('consultations.urls')),
    path('records/', include('records.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointment/', include('appointment.urls')),

    
]

# For media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)