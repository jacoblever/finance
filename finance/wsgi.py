"""
WSGI config for finance project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import logging
import os

from django.core.wsgi import get_wsgi_application

logging.basicConfig(
    filename='logs/webapp.log',
    format='%(asctime)s: %(levelname)s - %(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")

application = get_wsgi_application()
