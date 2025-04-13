from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from django.views.generic import TemplateView
from django.conf import settings

from utils.logger import LoggerHandler
from utils.menu import Menu

class HomeView(TemplateView):
    """
    Class-based view that renders the main homepage template.

    This view extends Django's TemplateView and is responsible for displaying
    the home page of the application. Additionally, it logs an informational
    message when the view is loaded.

    Attributes:
        template_name (str): The path to the HTML template to render.
        logger (Logger): Logger instance used to log events.

    Logging:
        Logs a message indicating that the login was successful.
    """
    logger = LoggerHandler().get_logger()
    logger.info("The login was good.")
    template_name = 'home/home.html'

