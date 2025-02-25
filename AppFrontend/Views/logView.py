import os
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View

from energyProyect import settings

LOG_FILE_PATH = os.path.join(os.path.dirname(settings.BASE_DIR), "log.log")

# class LogTemplateView(TemplateView):
#     """Vista para mostrar la plantilla de logs"""
#     template_name = "home/content/logs.html"


class GetLogsView(View):
    """
    API View to fetch logs as a JSON response.

    This view handles GET requests to retrieve logs from a log file.
    If the log file exists, the content of the file is read and returned in JSON format.
    If the log file does not exist, a 404 response is returned with an appropriate error message.

    Methods:
    -------
    get(request)
        Handles GET requests to retrieve the logs from the log file and return them as a JSON response.
        If the log file is not found, it returns a 404 response with an error message.
    """
    def get(self, request):
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
                logs = file.readlines()
            return JsonResponse({"logs": logs})
        else:
            return JsonResponse({"message": "Log file not found"}, status=404)
