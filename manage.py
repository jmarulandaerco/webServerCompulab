# manage.py
import os
import sys
from django.core.management import execute_from_command_line
from django.db.utils import OperationalError

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energyProyect.settings')
    try:
        # Configura Django
        import django
        django.setup()

        # Importa Menu después de configurar Django
        from utils.menu import Menu

        # Ejecuta la función solo al iniciar el servidor
        if 'runserver' in sys.argv:
            menu = Menu()
            menu.create_user_if_not_exists("erco_to","3rc04dm1n#t0")
            menu.create_user_if_not_exists("erco_config","3rc04dm1n#t0")


    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    try:
        main()
    except OperationalError:
        print("⚠️ No hay conexión a la base de datos, pero el servidor sigue funcionando...")
