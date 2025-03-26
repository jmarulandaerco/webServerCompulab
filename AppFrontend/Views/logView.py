import os
import zipfile
from django.http import FileResponse, JsonResponse
from django.views.generic import TemplateView
from django.views import View
from rest_framework.views import APIView

from energyProyect import settings

LOG_FILE_PATH = "/var/log/enrg/utilitymanager/log.log"
LOG_FILE_SINGLE_DEVICE="/var/log/enrg/modbus_read.log"
LOG_FILES = [LOG_FILE_PATH, os.path.join(settings.BASE_DIR, "django_log.log")]  # Ajusta las rutas de los archivos


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

class GetLogSingleDeviceView(APIView):
    
    """
    View that handles GET requests to retrieve the log entries of a single device from a log file.

    This view reads a log file and returns its content as a JSON response. If the log file exists,
    the response contains the lines from the file. If the log file is not found, an error message
    is returned with a 404 status code.

    Methods:
    --------
    get(request):
        Handles GET requests. If the log file exists, it returns the content of the file as a JSON response.
        If the file is not found, it returns an error message with a 404 status code.
    """
    

    def get(self, request):
        if os.path.exists(LOG_FILE_SINGLE_DEVICE):
            with open(LOG_FILE_SINGLE_DEVICE, "r", encoding="utf-8") as file:
                logs = file.readlines()
            return JsonResponse({"logs": logs})
        else:
            return JsonResponse({"message": "Log file not found"}, status=404)




class DownloadLogsView(View):
    """
    API View to download logs as a text file.

    This view handles GET requests to provide a downloadable log file.
    If the log file exists, it is returned as a downloadable response.
    If the log file does not exist, a 404 response is returned with an error message.

    Methods:
    -------
    get(request)
        Handles GET requests to provide the log file as a downloadable response.
        If the log file is not found, it returns a 404 response.
    """

    def get(self, request):
        zip_filename = "logs.zip"
        zip_path = os.path.join("/tmp", zip_filename)  # Guardar temporalmente el ZIP

        with zipfile.ZipFile(zip_path, "w") as zipf:
            files_added = False
            for log_file in LOG_FILES:
                if os.path.exists(log_file):
                    zipf.write(log_file, os.path.basename(log_file))
                    files_added = True

        if files_added:
            return FileResponse(open(zip_path, "rb"), as_attachment=True, filename=zip_filename)
        else:
            return JsonResponse("No log files found")

