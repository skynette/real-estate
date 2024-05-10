"""
ASGI config for zcore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

ENVIRONMENT = os.getenv('ENVIRONMENT', 'zcore.settings.development')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', ENVIRONMENT)

application = get_asgi_application()
