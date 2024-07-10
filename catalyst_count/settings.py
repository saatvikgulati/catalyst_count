"""
Django settings for catalyst_count project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Load environment variables from .env
env_path = BASE_DIR / '.env'
load_dotenv(env_path)
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG'))
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'app.apps.AppConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'bootstrap4',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

ROOT_URLCONF = 'catalyst_count.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'catalyst_count.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'OPTIONS': {
            'options': '-c search_path=catalyst_count'
        },
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = os.getenv('MEDIA_URL')
STATIC_URL = os.getenv('STATIC_URL')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR),
]
LOGIN_URL = os.getenv('LOGIN_URL')
LOGIN_REDIRECT_URL = os.getenv('LOGIN_REDIRECT_URL')
LOGOUT_URL = os.getenv('LOGOUT_URL')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
CRISPY_TEMPLATE_PACK = os.getenv('CRISPY_TEMPLATE_PACK')
CRISPY_ALLOWED_TEMPLATE_PACKS = os.getenv('CRISPY_ALLOWED_TEMPLATE_PACKS')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ACCOUNT_AUTHENTICATION_METHOD = os.getenv('ACCOUNT_AUTHENTICATION_METHOD')
ACCOUNT_EMAIL_REQUIRED = bool(os.getenv('ACCOUNT_EMAIL_REQUIRED'))
ACCOUNT_EMAIL_VERIFICATION = os.getenv('ACCOUNT_EMAIL_VERIFICATION')
ACCOUNT_USERNAME_REQUIRED = bool(os.getenv('ACCOUNT_USERNAME_REQUIRED'))
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = bool(os.getenv('ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE'))
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = int(os.getenv('ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS'))
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = bool(os.getenv('ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE'))

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = bool(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = bool(os.getenv('EMAIL_USE_TLS'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
API_URL = os.getenv('API_URL')
