# -*- coding: utf-8 -*-
"""
Production Configurations

- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails
- Use Redis for cache


"""
from __future__ import absolute_import, unicode_literals

from boto.s3.connection import OrdinaryCallingFormat
from django.utils import six


from .common import *  # noqa


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/1.9/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/ja/1.9/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_CONTENT_TYPE_NOSNIFF = os.environ.get(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', 'True') == 'True'
SECURE_BROWSER_XSS_FILTER = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SECURE_SSL_REDIRECT = os.environ.get(
    'DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = 'DENY'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split()
# END SITE CONFIGURATION

INSTALLED_APPS += ('gunicorn', )


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

AWS_ACCESS_KEY_ID = os.environ.get('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.

#  See:http://stackoverflow.com/questions/10390244/
from storages.backends.s3boto import S3BotoStorage
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')
DEFAULT_FILE_STORAGE = 'config.settings.production.MediaRootS3BotoStorage'

MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME

# Static Assets
# ------------------------

STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'config.settings.production.StaticRootS3BotoStorage'
# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before
# 'django.contrib.staticfiles'
AWS_PRELOAD_METADATA = True
INSTALLED_APPS = ('collectfast', ) + INSTALLED_APPS
# COMPRESSOR
# ------------------------------------------------------------------------------
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_URL = STATIC_URL
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', 'True') == 'True'
# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL',
                                    'devtinder <noreply@example.com>')
EMAIL_SUBJECT_PREFIX = os.environ.get('DJANGO_EMAIL_SUBJECT_PREFIX',
                                      '[devtinder] ')
SERVER_EMAIL = os.environ.get('DJANGO_SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ("anymail", )
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get('DJANGO_MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_SENDER_DOMAIN')
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# CACHING
# ------------------------------------------------------------------------------

REDIS_LOCATION = '{0}/{1}'.format(os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379'), 0)
# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}

# Custom Admin URL, use {% url 'admin:index' %}
ADMIN_URL = os.environ.get('DJANGO_ADMIN_URL', 'admin')

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
