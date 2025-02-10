import os
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View

from energyProyect import settings

LOG_FILE_PATH = os.path.join(settings.BASE_DIR, "log.log")

class LogTemplateView(TemplateView):
    """Vista para mostrar la plantilla de logs"""
    template_name = "home/content/logs.html"


class GetLogsView(View):
    """API para obtener los logs como JSON"""
    def get(self, request):
        print(os.path.exists(LOG_FILE_PATH))
        print("prepago")
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
                logs = file.readlines()
            return JsonResponse({"logs": logs})
        else:
            return JsonResponse({"error": "Archivo de log no encontrado"}, status=404)
