import os
from pathlib import Path
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Security settings – use environment variables in production
# ------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-3%y3laftm62q0zaj+s7#p-xqq9(&#q+)s8)p-&#&bz*0$!xu$0')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Defaults to False

# ------------------------------------------------------------------
# Hosts & trusted origins – Render sets RENDER_EXTERNAL_HOSTNAME
# ------------------------------------------------------------------
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])

CSRF_TRUSTED_ORIGINS = []
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    CSRF_TRUSTED_ORIGINS.append(f'https://{os.environ["RENDER_EXTERNAL_HOSTNAME"]}')

SITE_ID = 1

# ------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # works fine on PythonAnywhere & Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jewelryshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_preprocessors.store_menu',
                'store.context_preprocessors.cart_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'jewelryshop.wsgi.application'

# ------------------------------------------------------------------
# Database – SQLite (local), MySQL (PythonAnywhere), PostgreSQL (Render)
# ------------------------------------------------------------------
if os.environ.get('ON_PYTHONANYWHERE') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['PA_MYSQL_NAME'],
            'USER': os.environ['PA_MYSQL_USER'],
            'PASSWORD': os.environ['PA_MYSQL_PASSWORD'],
            'HOST': os.environ['PA_MYSQL_HOST'],
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }
elif 'DATABASE_URL' in os.environ:
    # ------------------- Render (PostgreSQL) -------------------
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # ------------------- Local development (SQLite) -------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static & media files (WhiteNoise handles static in production)
# ------------------------------------------------------------------
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'jewelryshop/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------
# Email – Resend (production) / console (development)
# ------------------------------------------------------------------
import resend

RESEND_API_KEY = os.environ.get('RESEND_API_KEY')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Only raise error if we are NOT running a management command (like collectstatic)
    import sys
    if 'collectstatic' not in sys.argv and not RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY environment variable is not set in production!")
    EMAIL_BACKEND = 'store.email_backend.ResendEmailBackend'
    DEFAULT_FROM_EMAIL = 'onboarding@resend.dev'

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ------------------------------------------------------------------
# Security settings for Render (HTTPS / proxy)
# ------------------------------------------------------------------
if not DEBUG and os.environ.get('RENDER'):
    # Tell Django that the proxy (Render) sends HTTPS traffic
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # Enforce secure cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True