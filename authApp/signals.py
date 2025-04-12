from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    users = [
        ("erco_to", "3rc04dm1n#t0"),
        ("erco_config", "3rc04dm1n#t0"),
    ]

    for username, password in users:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            logger.info(f"✅ Usuario '{username}' creado.")
        else:
            logger.info(f"⚠️ Usuario '{username}' ya existe.")
