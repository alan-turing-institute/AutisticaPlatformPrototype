"""
Django settings for oh_app_demo project.
"""

import os
from django.utils.translation import ugettext_lazy

# import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Customization for Heroku-specific settings
ON_HEROKU = os.getenv('ON_HEROKU', 'false').lower() == 'true'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'whopsthereshouldbeone')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True ##if os.getenv('DEBUG', '').lower() == 'true' else False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'openhumans',
    'skeleton.apps.Main',
    'StepperComponent.apps.UserjourneyConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'main_app.urls'

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

WSGI_APPLICATION = 'main_app.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

SESSION_ENGINE= 'django.contrib.sessions.backends.cached_db'


# Password validation

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

# Default language
LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Language/translation configurations

LANGUAGES = (
    ('en', ugettext_lazy('English')),
    ('fr', ugettext_lazy('French')),
)

# Tell Django where the project's translation files should be.
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'skeleton': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}


##################################################
# Custom app settings
#
# Configure these with .env/environment variables

# After log in, send users to the overview page.
LOGIN_REDIRECT_URL = 'overview'

# Project's page on Open Humans
OH_PROJ_PAGE = os.getenv(
    'OH_PROJ_PAGE', '')

# Open Humans settings
OPENHUMANS_APP_BASE_URL = os.getenv(
    'OPENHUMANS_APP_BASE_URL', 'http://localhost:5000')
OPENHUMANS_CLIENT_ID = os.getenv('OPENHUMANS_CLIENT_ID', 'your_client_id')
OPENHUMANS_CLIENT_SECRET = os.getenv(
    'OPENHUMANS_CLIENT_SECRET', 'your_client_secret')

# Admin account password for configuration.
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')

#DataFlair #Django #Static files
STATIC_URL = '/static/'
#--------------------------------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#-----------------------------------------------------
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
]

# if ON_HEROKU:
#     SECURE_SSL_REDIRECT = True
#     django_heroku.settings(locals())

# REMOVE IN PROD
X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
