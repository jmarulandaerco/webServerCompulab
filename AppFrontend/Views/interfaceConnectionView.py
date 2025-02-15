import json
import os
from django.http import JsonResponse
from django.views import View

class InterfaceConnection(View):
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

            return JsonResponse({"message": "Configuración aplicada correctamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
