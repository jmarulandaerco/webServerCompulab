from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from django.views.generic import TemplateView
from django.conf import settings

class HomeView(TemplateView):
    template_name = 'home/home.html'

