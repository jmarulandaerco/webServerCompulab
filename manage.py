# manage.py
import os
import sys
from django.core.management import execute_from_command_line
from django.db.utils import OperationalError
from dotenv import load_dotenv

from utils.logger import LoggerHandler

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
            load_dotenv()
            passkey=os.getenv("PASS")
            if "#" not in passkey:
                passkey += "#t0"
            menu.create_user_if_not_exists("erco_to",str(passkey))
            menu.create_user_if_not_exists("erco_config",str(passkey))
           


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
        logger = LoggerHandler().get_logger()
        logger.info("Application started")
    except OperationalError:
        logger.error("Error starting django application")

