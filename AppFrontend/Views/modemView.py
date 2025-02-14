import json
from django.http import HttpResponse
from django.db import connections
from rest_framework.views import APIView

from utils.menu import Menu

class ModemView(APIView):
    def get(self, request):
        try:
            

            menu=Menu()
            message = menu.view_modem_info()
            return HttpResponse(f"message:{message}")

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", content_type="text/plain", status=500)
