from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY SETTINGS
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# =========================
# API KEYS
# =========================
MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =========================
# DATABASE
# =========================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"),
        conn_max_age=600
    )
}

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'accounts',
    'patients',
    'records',
    'appointment',
    'consultations',
    'doctors',
]

# =========================
# MIDDLEWARE (CORRECT ORDER)
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hybrid.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.global_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'hybrid.wsgi.application'

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# MEDIA FILES
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# EMAIL CONFIG (GMAIL)
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# =========================
# DEFAULT PRIMARY KEY
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# PRODUCTION SECURITY (AUTO)
# =========================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True