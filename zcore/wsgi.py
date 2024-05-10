"""
WSGI config for zcore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENVIRONMENT = os.getenv('ENVIRONMENT', 'zcore.settings.development')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', ENVIRONMENT)

application = get_wsgi_application()
