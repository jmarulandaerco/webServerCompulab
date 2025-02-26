import json
import os
import subprocess
from django.http import JsonResponse
from rest_framework.views import APIView

from utils.menu import Menu

class InterfaceConnection(APIView):
    """
    API View for configuring network interface connections.

    This view handles POST requests to configure an interface connection with a given IP address and gateway.
    The data must include a valid IP and optionally a gateway.
    It uses the `nmcli` command to apply the configuration.

    Methods:
    -------
    post(request, connection_name)
        Handles POST requests to configure the network connection with the given connection name.
    """
    def post(self, request, connection_name):
        try:
            # Cargar datos JSON
            data = json.loads(request.body)
            ip = data.get("ip")
            gateway = data.get("gateway")

            # Validar que los valores no sean nulos o vacíos
            if not ip:
                return JsonResponse({"message": "Invalid IP address"}, status=400)

            # Construir comando de manera segura
            command = ["sudo", "nmcli", "con", "mod", connection_name, "ipv4.addresses", ip]
            if gateway:
                command += ["ipv4.gateway", gateway]
            command += ["ipv4.method", "manual"]

            # Ejecutar el comando de forma segura
            result = subprocess.run(command, capture_output=True, text=True)

            # Verificar si hubo errores
            if result.returncode != 0:
                return JsonResponse({"message": f"Error configuring network: {result.stderr}"}, status=500)

            return JsonResponse({"message": "Configuration correctly applied"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)


class AntennaWifi(APIView):
    """
    API View for toggling the status of the WiFi antenna.

    This view handles GET requests to toggle the WiFi antenna on or off using the `Menu` class.

    Methods:
    -------
    get(request)
        Handles GET requests to toggle the WiFi antenna and returns its status.
    """
    def get(self, request):
        try:
            menu = Menu()
            status=menu.toggle_wifi()
            return JsonResponse({"message": f"{status}"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class AddWifi(APIView):
    """
    API View for adding a WiFi connection.

    This view handles POST requests to add a new WiFi network with the provided SSID, password, and connection name.
    It uses the `Menu` class to add the WiFi network.

    Methods:
    -------
    post(request)
        Handles POST requests to add a WiFi network with the provided SSID, password, and connection name.
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            ssid = data.get("ssid")
            password = data.get("password")
            name = data.get("name")
            menu = Menu()
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            response = menu.add_wifi(ssid=ssid,password=password,connection_name=name)
            

            
            return JsonResponse({"message": f"{response}"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
