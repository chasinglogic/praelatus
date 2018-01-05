"""
Django settings for the praelatus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import yaml

from socket import gethostname

from .celery import app as celery_app

__all__ = ['celery_app']

# Project settings, Not CONFIGurable
RELEASE_NAME = 'Rio Bravo'
VERSION = '0.1.0'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.getenv('PRAELATUS_DATA_DIR', os.path.join(BASE_DIR, 'data'))
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

APPEND_SLASH = False

# SECURITY WARNING: keep the secret key used in production secret!
if os.path.exists(os.path.join(DATA_DIR, '.secret_key')):
    with open(os.path.join(DATA_DIR, '.secret_key')) as f:
        SECRET_KEY = f.read()
else:
    with open(os.path.join(DATA_DIR, '.secret_key'), 'w') as f:
        import binascii
        rand = os.urandom(128)
        SECRET_KEY = binascii.b2a_hex(rand).decode('ascii')
        f.write(SECRET_KEY)

INSTALLED_APPS = [
    # Row level security
    'guardian',
    # Filtering of models
    'django_filters',
    # REST API
    'rest_framework',

    # TODO: NOT COMPATIBLE WITH DJANGO 2 Need to not use github version
    # Github-esque notifications
    # https://github.com/django-notifications/django-notifications
    'notifications',

    # Praelatus
    'projects.apps.ProjectsConfig',
    'tickets.apps.TicketsConfig',
    'profiles.apps.ProfilesConfig',
    'queries.apps.QueriesConfig',
    'schemes.apps.SchemesConfig',
    'workflows.apps.WorkflowsConfig',
    'labels.apps.LabelsConfig',
    'fields.apps.FieldsConfig',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'praelatus.urls'


def version_number(request):
    return {'version_number': VERSION}


def release_name(request):
    return {'release_name': RELEASE_NAME}


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'praelatus.settings.version_number',
            'praelatus.settings.release_name',
        ],
    },
}]

WSGI_APPLICATION = 'praelatus.wsgi.application'

# AUTHENTICATION
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/tickets/dashboard'
LOGOUT_REDIRECT_URL = '/'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_PROFILE_MODULE = 'profiles.Profile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'projects.backends.ObjectPermissionAnonFallbackBackend',
    'guardian.backends.ObjectPermissionBackend', )

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# REST

REST_FRAMEWORK = {
    # Integrate Django Filters
    'DEFAULT_FILTER_BACKENDS':
    ('django_filters.rest_framework.DjangoFilterBackend', ),

    # Use sessions or basic auth
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework.authentication.BasicAuthentication',
     'rest_framework.authentication.SessionAuthentication', ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES':
    ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly']
}


X_FRAME_OPTIONS = 'DENY'

# Project CONFIG, these are taken from the praelatus CONFIG file
try:
    with open(os.path.join(DATA_DIR, 'config.yaml')) as f:
        CONFIG = yaml.load(f)
except FileNotFoundError:
    CONFIG = {
        'https': ('true' == os.getenv('PRAE_HTTPS_ENABLED', 'false').lower()),
        'debug': ('true' == os.getenv('PRAE_DEBUG', 'false').lower()),
        'allowed_hosts':
        os.getenv('PRAE_ALLOWED_HOSTS', gethostname()).split(','),
        'session_engine':
        os.getenv('PRAE_SESSION_ENGINE',
                  'django.contrib.sessions.backends.cached_db'),
        'database': {
            'default': {
                'ENGINE':
                os.getenv('PRAE_DB_ENGINE', 'django.db.backends.postgresql'),
                'NAME':
                os.getenv('PRAE_DB_NAME', 'praelatus'),
                'USER':
                os.getenv('PRAE_DB_USER', 'postgres'),
                'PASSWORD':
                os.getenv('PRAE_DB_PASS', 'postgres'),
                'HOST':
                os.getenv('PRAE_DB_HOST', '127.0.0.1'),
                'PORT':
                os.getenv('PRAE_DB_PORT', '5432')
            }
        },
        'language_code':
        os.getenv('PRAE_LANG_CODE', 'en-us'),
        'time_zone':
        os.getenv('PRAE_TZ', 'UTC'),
        'use_tz':
        bool(os.getenv('PRAE_USE_TZ', 'true')),
        'use_i18n':
        bool(os.getenv('PRAE_ENBALE_INTERNATIONALIZATION', 'true')),
        'static_root':
        os.getenv('PRAE_STATIC_ROOT', os.path.join(DATA_DIR, 'static')),
        'media_root':
        os.getenv('PRAE_MEDIA_ROOT', os.path.join(DATA_DIR, 'media')),
        'cache': {
            'default': {
                'BACKEND':
                'django_redis.cache.RedisCache',
                'LOCATION':
                os.getenv('PRAE_REDIS_URL', 'redis://127.0.0.1:6379/1'),
                'KEY_PREFIX':
                'PRAE',
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient'
                }
            }
        },
        'mq_server':
        os.getenv('PRAE_MQ_SERVER', 'amqp://guest:guest@localhost:5672//'),
        'mq_result_backend':
        os.getenv('PRAE_MQ_RESULT', 'rpc://'),
        'email': {
            'backend':
            os.getenv('PRAE_EMAIL_BACKEND',
                      'django.core.mail.backends.smtp.EmailBackend'),
            'address':
            os.getenv('PRAE_EMAIL_ADDRESS', 'praelatus@' + gethostname()),
            'host':
            os.getenv('PRAE_EMAIL_HOST', 'localhost'),
            'port':
            int(os.getenv('PRAE_EMAIL_PORT', '25')),
            'user':
            os.getenv('PRAE_EMAIL_USER', None),
            'pass':
            os.getenv('PRAE_EMAIL_PASS', None),
            'use_tls': ('true' == os.getenv('PRAE_EMAIL_USE_TLS', 'false').lower()),
            'use_ssl': ('true' == os.getenv('PRAE_EMAIL_USE_TLS', 'false').lower()),
        }
    }

if CONFIG.get('https', False):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('debug', False)
ALLOWED_HOSTS = CONFIG.get('allowed_hosts', [])
SESSION_ENGINE = CONFIG.get('session_engine')
DATABASES = CONFIG.get('database')

# Internationalization
LANGUAGE_CODE = CONFIG.get('language_code')
TIME_ZONE = CONFIG.get('time_zone')
USE_I18N = CONFIG.get('use_i18n')
USE_TZ = CONFIG.get('use_tz')

STATIC_ROOT = CONFIG.get('static_root')
MEDIA_ROOT = CONFIG.get('media_root')

# CACHING

CACHES = CONFIG.get('cache')

# CELERY

CELERY_BROKER_URL = CONFIG.get('mq_server')
CELERY_RESULT_BACKEND = CONFIG.get('mq_result_backend')

# EMAIL

EMAIL_BACKEND = CONFIG.get('email', {}).get('backend')
EMAIL_ADDRESS = CONFIG.get('email', {}).get('address')
EMAIL_HOST = CONFIG.get('email', {}).get('host')
EMAIL_PORT = CONFIG.get('email', {}).get('port')
EMAIL_HOST_USER = CONFIG.get('email', {}).get('username')
EMAIL_HOST_PASS = CONFIG.get('email', {}).get('password')
EMAIL_USE_TLS = CONFIG.get('email', {}).get('use_tls')
EMAIL_USE_SSL = CONFIG.get('email', {}).get('use_ssl')
