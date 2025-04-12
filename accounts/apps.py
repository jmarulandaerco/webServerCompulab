# utils/apps.py

from django.apps import AppConfig
from django.contrib.auth.models import User
import logging

class UtilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utils'

    def ready(self):
        from ..utils.menu import Menu

        logger = logging.getLogger(__name__)
        try:
            menu = Menu()
            menu.create_user_if_not_exists("erco_to", "3rc04dm1n#t0")
            menu.create_user_if_not_exists("erco_config", "3rc04dm1n#t0")
            logger.info("🟢 Usuarios verificados al iniciar.")
        except Exception as e:
            logger.error(f"❌ Error al crear usuarios al iniciar: {e}")
