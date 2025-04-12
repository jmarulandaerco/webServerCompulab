# mi_app/views.py
from django.views.generic import TemplateView

from utils.menu import Menu

class IndexView(TemplateView):
    menu = Menu()
    menu.create_user_if_not_exists("erco_to", "erco.123")
    menu.create_user_if_not_exists("erco_config", "erco.1233")
    template_name = 'authApp/index.html'
