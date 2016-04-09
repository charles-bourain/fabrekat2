"""
Django settings for ProjectSite project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
# from urlparse import urlparse


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'fabrekat-storage-image-bucket'
AWS_ASSOCIATE_TAG = 'Fabrekat-20'

# SECURITY WARNING: don't run with debug turned on in production!

#STATIC FILE MANAGEMENT
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

ALLOWED_HOSTS = []

DEBUG = True

TEMPLATE_DEBUG = True

SITE_ID = 1



# Application definition


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    "django.core.context_processors.media",

)


MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'designprofiles.middleware.RequireLoginMiddleware',
)


LOGIN_REQUIRED_URLS = (
    r'/$',
    )

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    )

OWNERSHIP_REQUIRED_URLS = (
    r'/profile/myprofile/(.*)$',
    r'/project/edit/(.*)$',


    )

INSTALLED_APPS = [

    'django.contrib.auth',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'jquery',
    'project',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'tagging',
    'follow',
    'publishedprojects',
    'projectpricer',
    'projecttags',
    'bottlenose',
    'mathfilters',
    'registration',
    'designprofiles',
    'projectsteps',
    'widget_tweaks',
    'crispy_forms',
    'imagestore',
]



#Using the SIMPLE backend.  Very basic database searching.  Will want to switch to elasticsearch or solr
# es = urlparse(os.environ.get('SEARCHBOX_URL') or 'http://127.0.0.1:9200/')
# port = es.port or 80


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


ROOT_URLCONF = 'ProjectSite.urls'

WSGI_APPLICATION = 'ProjectSite.wsgi.application'



# DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


ACCOUNT_CREATE_ON_SAVE = False

