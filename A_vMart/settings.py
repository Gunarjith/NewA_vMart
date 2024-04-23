

from builtins import locals
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x%=)8%2w(##6u!gl^k)rbp4k3r-&w*%qqn(ifdz4%b7)(!zlz)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



ALLOWED_HOSTS = ['*']

DomainName = 'https://127.0.0.1:8000' + '/'
# Application definition

import logging

LOGIN_REQUIRED = True
LOGIN_URL = '/accounts/login/'
# accounts/login/
# Set Boto3's logging level to a higher level to suppress the detailed logs
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

INSTALLED_APPS = [
    #  'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'A_vMart',
    'A_Appointment',
    'A_webhook',
    'B_profile',
    'D_facebook',
    'G_payment',
    'K_Ticket',
    's_survey',
    'H_hotel',
    'crispy_forms',
    'storages',
    'corsheaders',
    'vailodb',
    'vailodb_n',
    'N_donation',
    'vailodb_b',
    'vailodb_a',
    'vailodb_s',
    'vailodb_h',


]

JAZZMIN_UI_TWEAKS = {

    "theme": "simplex",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ajax request object
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    # Add your allowed origins here, e.g.:
    'http://localhost:8000',
    'http://example.com',
]

ROOT_URLCONF = 'A_vMart.urls'

REGIR = os.path.join(BASE_DIR, 'templates')
TEMP_DIR = os.path.join(BASE_DIR, "templates/")

# added recently
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
# endof added recently
TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [REGIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'A_vMart.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vailodb',
        'USER': "root",
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES',foreign_key_checks = 0;",
            'charset': 'utf8mb4',
            'init_command': "SET collation_connection = 'utf8mb4_unicode_ci'",
        }

    }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
# Define the base URL for your media files in development and production
MEDIA_URL = '/media/'

# Define the static and media roots for development and production
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    # If you need media files to be served directly from your server in production
    # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # If you are using AWS S3 for media storage in production
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/E_product/static/images/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/E_product/static/images/')

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ADMIN_MEDIA_PREFIX = '/staticfiles/admin/'

# aws s3 Buckets config

AWS_ACCESS_KEY_ID = 'AKIA52X7F2GN5GDNHQ4Z'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'vailo.ai-bucket'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'vailo.ai7@gmail.com '
EMAIL_HOST_PASSWORD = 'rrgwtgvhycrjeywh'

# DEFAULT_FROM_EMAIL = 'contact@vailo.ai'

# SERVER_MAIL = 'contact@vailo.ai'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST= 'smtp.zoho.com'
# EMAIL_PORT=587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = 'contact@vailo.ai'
# EMAIL_HOST_PASSWORD = '123Vailo$'

# django_on_heroku.settings(locals())


# <?xml version="1.0" encoding="UTF-8"?>
# <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
#   <CORSRule>
#     <AllowedOrigin>https://example.org</AllowedOrigin>
#     <AllowedMethod>HEAD</AllowedMethod>
#     <AllowedMethod>GET</AllowedMethod>
#     <AllowedMethod>PUT</AllowedMethod>
#     <AllowedMethod>POST</AllowedMethod>
#     <AllowedMethod>DELETE</AllowedMethod>
#     <AllowedHeader>*</AllowedHeader>
#     <ExposeHeader>ETag</ExposeHeader>
#     <ExposeHeader>x-amz-meta-custom-header</ExposeHeader>
#   </CORSRule>
# </CORSConfiguration>

# For timezone
#TIME_ZONE = 'America/New_York'


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # You can use other backends as well
SESSION_COOKIE_SECURE = True  # Set it to True if using HTTPS
SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = 'Lax'  # Adjust the value based on your requirements

