import os
from django.conf import settings
import base

DATABASES = settings.DATABASES

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

#PRODUCTION SPECIFIC APPS
base.INSTALLED_APPS += [
    'whitenoise',
    'djrill',
    'storages',
]

print base.INSTALLED_APPS

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default='postgres://localhost'),
}
DATABASES['default']['CONN_MAX_AGE'] = 500


#STATIC FILE MANAGEMENT
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)



# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Allow all host headers
ALLOWED_HOSTS = ['*']



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

#EMAIL MANAGER (djrill)
MANDRILL_API_KEY = "3rxHtBbmRLBbLi4EgazU-A"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
DEFAULT_FROM_EMAIL = "Charles.Barrett@fabrekat.com"


#TEMPLATE MANAGEMENT
TEMPLATE_DIRS=(
    os.path.join(BASE_DIR, 'templates'),
    )

#MEDIA AND MEDIA STORAGE MANAGEMENT
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoSTorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'http://%s.s3-website-us-west-2.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

LOGIN_URL = '/account/login/'

