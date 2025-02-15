import json
from django.http import HttpResponse, JsonResponse
from django.db import connections
from rest_framework.views import APIView

from utils.menu import Menu

class ModemView(APIView):
    def get(self, request):
        try:
            

            menu=Menu()
            message = menu.view_modem_info()
           
            return JsonResponse({"message":message})

        except Exception as e:
            return JsonResponse({"message":message})
