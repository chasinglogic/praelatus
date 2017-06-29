"""
Django settings for the praelatus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import yaml

from .celery import app as celery_app

__all__ = ['celery_app']

# Project settings, Not configurable
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
        rand = os.urandom(24)
        SECRET_KEY = binascii.b2a_hex(rand).decode('ascii')
        f.write(SECRET_KEY)


INSTALLED_APPS = [
    # Row level security
    'guardian',
    # Filtering of models
    'django_filters',
    # REST API
    'rest_framework',
    # Github-esque notifications
    # https://github.com/django-notifications/django-notifications
    'notifications',

    # Praelatus
    'projects.apps.ProjectsConfig',
    'workflows.apps.WorkflowsConfig',
    'tickets.apps.TicketsConfig',
    'labels.apps.LabelsConfig',
    'fields.apps.FieldsConfig',
    'profiles.apps.ProfilesConfig',
    'queries.apps.QueriesConfig',
    'hooks.apps.HooksConfig',
    'upvotes.apps.UpvotesConfig',
    'schemes.apps.SchemesConfig',
    'links.apps.LinksConfig',

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


TEMPLATES = [
    {
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
    }
]

WSGI_APPLICATION = 'praelatus.wsgi.application'

# AUTHENTICATION
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/tickets/dashboard'
LOGOUT_REDIRECT_URL = '/'
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

AUTH_PROFILE_MODULE = 'profiles.Profile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# REST

REST_FRAMEWORK = {
    # Integrate Django Filters
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    # Use sessions or basic auth
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Project config, these are taken from the praelatus config file
try:
    with open(os.path.join(DATA_DIR, 'config.yaml')) as f:
        config = yaml.load(f)
except FileNotFoundError:
    import sys
    if 'genconfig' not in sys.argv:
        print('No config file found, run ./manage.py genconfig.'
              'See https://docs.praelatus.io/deployments/Deploy%20on%20Linux/#configuring-praelatus'
              'for more information.')
    config = {}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('debug', False)
ALLOWED_HOSTS = config.get('allowed_hosts', [])
SESSION_ENGINE = config.get('session_engine',
                            'django.contrib.sessions.backends.cached_db')
DATABASES = config.get('database', {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'praelatus',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
})

# Internationalization
LANGUAGE_CODE = config.get('language_code', 'en-us')
TIME_ZONE = config.get('time_zone', 'UTC')
USE_I18N = config.get('use_i18n', True)
USE_L10N = config.get('use_l10n', True)
USE_TZ = config.get('use_tz', True)

STATIC_ROOT = config.get('static_root', os.path.join(DATA_DIR, 'static'))
MEDIA_ROOT = config.get('media_root', os.path.join(STATIC_ROOT, 'media'))

# CACHING

CACHES = config.get('cache', {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'KEY_PREFIX': 'PRAE',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
})

# CELERY

CELERY_BROKER_URL = config.get('mq_server', CACHES['default']['LOCATION'])
CELERY_RESULT_BACKEND = 'rpc://'

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_ADDRESS = config.get('email', {}).get('address', 'praelatus@localhost')
EMAIL_HOST = config.get('email', {}).get('host', 'localhost')
EMAIL_PORT = config.get('email', {}).get('port', 25)
EMAIL_HOST_USER = config.get('email', {}).get('username', None)
EMAIL_HOST_PASS = config.get('email', {}).get('password', None)
EMAIL_USE_TLS = config.get('email', {}).get('use_tls', False)
EMAIL_USE_SSL = config.get('email', {}).get('use_ssl', False)
