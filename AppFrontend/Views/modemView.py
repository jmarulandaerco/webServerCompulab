import json
import subprocess
from django.http import HttpResponse, JsonResponse
from django.db import connections
from rest_framework.views import APIView
import netifaces

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
            
            data = json.loads(request.body)
            device = data.get("device_type")
            menu=Menu()
            message = menu.view_modem_info(device)
           
            return JsonResponse({"message":message})

        except Exception as e:
            return JsonResponse({"message":message})


class InterfaceIPView(APIView):
    """
    Retrieves the IP address and gateway of a given network interface.

    GET:
    - URL parameter: `interface` (str) - Name of the network interface.
    - Calls `Menu.get_ip_interface(interface)` and `Menu.get_gateway_interface(interface)` 
      to obtain the IP and gateway of the specified interface.

    Responses:
    - 200 OK: Returns JSON with the interface name, IP address, and gateway (if available).
        Example: {"interface": "eth0", "ip": "192.168.1.10", "gateway": "192.168.1.1"}
    - 400 Bad Request: If the IP cannot be retrieved. This usually indicates that the interface
      is disconnected or does not have a configured IP.
        Example: {"message": "Could not retrieve the IP for eth0. Check physical connection or if the interface has no configured IP."}
    """
    def get(self, request, interface):
        menu=Menu()
        ip = menu.get_ip_interface(interface)
        gateway=menu.get_gateway_interface(interface)

        if ip:
            if not gateway:
                # Define el comando
                cmd = [['sudo', 'ip', 'route', 'del', 'default', 'dev', 'eth0'],['sudo', 'ip', 'route', 'del', 'default', 'dev', 'eth1']]

                for i in cmd:
                    try:   
                        result = subprocess.run(i, check=True, text=True, capture_output=True)
                    except:
                        print("Hola")
                
                return JsonResponse({'interface': interface, 'ip': f"{ip}/24",'gateway':''})
            else:
                return JsonResponse({'interface': interface, 'ip': f"{ip}/24",'gateway':gateway})
        else:
            return JsonResponse(
                {'message': f'No se pudo obtener la Ip {interface}. Verifica la conexión física o que la interfaz no tenga una IP sin configurar'},status=400
               
            )


class Wlan(APIView):
    
    
    permission_classes = []         # ajusta según tu autenticación
    authentication_classes = []

    def get(self, request):
        menu = Menu()

        for iface in netifaces.interfaces():
            if iface.startswith('wlan'):
                ip = menu.get_wlan_ip(iface)
                if ip is not None:
                    # Éxito: enviamos únicamente la IP
                    return JsonResponse({'message': ip}, status=200)
                # Error: no hay IP en esta interfaz
                return JsonResponse(
                    {'message': f'No se pudo obtener la IP en {iface}. Verifica la conexión WLAN.'},
                    status=400
                )

        # No encontró ninguna interfaz wlan*
        return JsonResponse(
            {'message': 'No se detectaron interfaces wlan en este dispositivo.'},
            status=404
        )
