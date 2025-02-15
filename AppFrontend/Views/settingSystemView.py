import json
import os
from django.http import JsonResponse
from rest_framework.views import APIView

from utils.menu import Menu

class InterfaceConnection(APIView):
    def post(self, request, connection_name):
        try:
            data = json.loads(request.body)
            ip = data.get("ip")
            gateway = data.get("gateway")

            command = f"sudo nmcli con mod '{connection_name}' ipv4.addresses '{ip}'"
            if gateway:
                command += f" ipv4.gateway '{gateway}'"
            command += " ipv4.method 'manual'"

            os.system(command)
            print(command)
            return JsonResponse({"message": "Configuración aplicada correctamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class AntennaWifi(APIView):
    def get(self, request):
        try:
            menu = Menu()
            status=menu.toggle_wifi()
            return JsonResponse({"message": f"{status}"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class AddWifi(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            ssid = data.get("ssid")
            password = data.get("password")
            name = data.get("name")
            menu = Menu()
            response = menu.add_wifi(ssid=ssid,password=password,connection_name=name)

            
            return JsonResponse({"message": f"{response}"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
