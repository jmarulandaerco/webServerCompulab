"""
WSGI config for authProyect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from utils.menu import Menu

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energyProyect.settings')

application = get_wsgi_application()

menu = Menu()
menu.create_user_if_not_exists("erco_to", "3rc04dm1n#t0")
menu.create_user_if_not_exists("erco_config", "3rc04dm1n#t0")