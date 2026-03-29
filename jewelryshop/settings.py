import os
import pymysql
from pathlib import Path
import dj_database_url

# MySQL compatibility
pymysql.install_as_MySQLdb()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings – use environment variables in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-3%y3laftm62q0zaj+s7#p-xqq9(&#q+)s8)p-&#&bz*0$!xu$0')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'e-commerce-web.up.railway.app',
]
# Add this to fix CSRF errors
CSRF_TRUSTED_ORIGINS = ['https://e-commerce-web.up.railway.app']

# Application definition
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
    'whitenoise.middleware.WhiteNoiseMiddleware',   # <-- add this line
    'django.middleware.security.SecurityMiddleware',
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

# Database
# -----------------------------------------------------------------
# Use DATABASE_URL if set (e.g., on Railway or custom MySQL), otherwise fallback to SQLite.
# For MySQL, set DATABASE_URL like:
#   mysql://USER:PASSWORD@HOST:PORT/DBNAME
# Example: mysql://root:password@localhost:3306/jewelryshop_db
# To create the database, run: CREATE DATABASE jewelryshop_db CHARACTER SET utf8mb4;
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# 1. Where Django looks for static files during development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'jewelryshop/static'),
]

# 2. Where Django MOVES all files for production (Railway)
# Change the name to 'staticfiles' to avoid conflicts with your source folders
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# 3. The URL used to access these files in the browser
STATIC_URL = '/static/'

# Whitenoise compression and caching (optional but recommended)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#setting email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS= True
EMAIL_PORT= 587
EMAIL_HOST_USER='adithyan.m.2742001@gmail.com'
EMAIL_HOST_PASSWORD= 'fwuk umwc nzaa hcwp'



