import json
from django.http import HttpResponse, JsonResponse
from django.db import connections
from rest_framework.views import APIView

from utils.menu import Menu

class ModemView(APIView):
    """
    API View for retrieving modem information.

    This view handles GET requests to fetch the current modem information.
    It uses the `Menu` class to retrieve modem data and return it as a JSON response.
    If an error occurs during the process, it catches the exception and returns an error message.

    Methods:
    -------
    get(request)
        Handles GET requests to retrieve modem information.
    """
    def get(self, request):
        try:
            

            menu=Menu()
            message = menu.view_modem_info()
           
            return JsonResponse({"message":message})

        except Exception as e:
            return JsonResponse({"message":message})
