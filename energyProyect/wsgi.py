"""
WSGI config for authProyect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energyProyect.settings')

# Asegura que Django esté completamente configurado antes de usar modelos o utilidades
django.setup()

# Ahora se puede acceder con seguridad a cualquier lógica que dependa de Django
from utils.menu import Menu

menu = Menu()
menu.create_user_if_not_exists("erco_to", "3rc04dm1n#t0")
menu.create_user_if_not_exists("erco_config", "3rc04dm1n#t0")

application = get_wsgi_application()
