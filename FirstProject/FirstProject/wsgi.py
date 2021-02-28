"""
WSGI config for FirstProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

setting_module = 'FirstProject.settings' if 'WEBSITE_HOSTNAME' in os.environ else 'FirstProject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
