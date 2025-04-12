from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from utils.menu import Menu
        menu = Menu()
        menu.create_user_if_not_exists("erco_to", "3rc04dm1n#t0")
        menu.create_user_if_not_exists("erco_config", "3rc04dm1n#t0")
