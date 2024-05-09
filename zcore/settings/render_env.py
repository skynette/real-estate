from .base import *

EMAIL_BACKEND = 'djcelery_email.backends.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = "info@realestate.com"
DOMAIN = os.environ.get("DOMAIN")
SITE_NAME = "Real Estate"

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('POSTGRES_NAME'),
		'USER': os.environ.get('POSTGRES_USER'),
		'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
		'HOST': os.environ.get('POSTGRES_HOST'),
		'PORT': os.environ.get('POSTGRES_PORT'),
	}
}


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND')
CELERY_TIMEZONE = "Africa/Lagos"
