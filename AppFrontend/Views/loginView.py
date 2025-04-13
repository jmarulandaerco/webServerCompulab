# mi_app/views.py
from django.views.generic import TemplateView

from utils.menu import Menu

    
class IndexView(TemplateView):
    """
    Class-based view that renders the main index page of the authentication app.

    This view extends Django's TemplateView and is responsible for rendering the
    index.html template located in the 'authApp' directory. It also ensures that
    specific users are created if they do not already exist.

    Attributes:
        template_name (str): The path to the HTML template to render.

    Side Effects:
        - Creates the user 'erco_to' with password 'erco.123' if not present.
        - Creates the user 'erco_config' with password 'erco.1233' if not present.
    """
    menu = Menu()
    menu.create_user_if_not_exists("erco_to", "3rc04dm1n#t0")
    menu.create_user_if_not_exists("erco_config", "3rc04dm1n#t0")
    template_name = 'authApp/index.html'
