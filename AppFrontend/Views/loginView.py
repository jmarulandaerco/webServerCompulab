# mi_app/views.py
from django.views.generic import TemplateView

from utils.menu import Menu

class IndexView(TemplateView):
    menu = Menu()
    menu.create_user_if_not_exists("erco_to", "3rc04dm1n#t0")
    menu.create_user_if_not_exists("erco_config", "3rc04dm1n#t0")
    template_name = 'authApp/index.html'
