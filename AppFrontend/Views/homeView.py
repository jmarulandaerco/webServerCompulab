from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from django.views.generic import TemplateView
from django.conf import settings

from utils.logger import LoggerHandler

class HomeView(TemplateView):
    logger = LoggerHandler().get_logger()
    logger.info("The login was good.")
    template_name = 'home/home.html'

