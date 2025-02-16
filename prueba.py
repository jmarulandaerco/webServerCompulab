# import os
# from django.contrib.auth.hashers import make_password

# # Establece el entorno de configuración
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authProyect.settings')

# # Ahora puedes usar las funciones de Django
# plain_password = "3rc0#4dm1n#t0"
# hashed_password = make_password(plain_password,"mMUj0DrIK6vgtdIYepkIxN")

# print(hashed_password)

import os
import django
from bson import ObjectId

from utils.menu import Menu  # Necesario para trabajar con ObjectId

# Configurar Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energyProyect.settings')
django.setup()

from authApp.models.user import User  # Importar modelos después de django.setup()

username = "erco_to"
password = "3rc04dm1n#t0"
username2 = "configTo"
password2 = "3rc04dm1n#t0"
menu = Menu()
menu.create_user_if_not_exists(username=username,password=password)