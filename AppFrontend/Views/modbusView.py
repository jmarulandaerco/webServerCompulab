import configparser
import json
import os
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from utils.configfiles import configfilepaths
from utils.menu import Menu


config = configparser.ConfigParser(interpolation=None)
cf = configfilepaths()
list_path_menu = cf.to_list()

class FormModbusView(View):
    def get(self, request):
        sample_data = {
            "debug": "DEBUG",
            "attempts": "3",
            "timeout": "1",
        }
        return JsonResponse(sample_data)
    

class FormModbusDevicesView(View):
    def get(self, request):
        device_param = request.GET.get('device', '')  # Obtener el string "device"
        print(f"Device recibido: {device_param}")

        if not device_param:  # Manejo si no se recibe el parámetro
            return HttpResponseNotFound("Error: No se especificó un dispositivo.")

        config.read(list_path_menu[2])
        menu = Menu()
        a = menu.setup_folder_path()
        print("Holiii")
        print(a)

        current_devices = config.sections()
        if "Default" in current_devices:
            current_devices.remove("Default")

        enabled_devices = config.get("Default", "devices_config", fallback="").split(",")

        listDevices = current_devices
        listSelectedDevices = enabled_devices

        print("Lista de dispositivos:", listDevices)
        print("Dispositivos habilitados:", listSelectedDevices)

        # Renderiza la plantilla basada en el parámetro recibido
        template_name = f'home/content/form/{device_param}.html'

        try:
             return render(request, f'home/content/form/{device_param}.html', {
            'listDevices': listDevices,
            'listSelectedDevices': listSelectedDevices
        })
        except:
            return HttpResponseNotFound(f"Error: La plantilla {template_name} no existe.")
        



class FormModbusGetDevicesView(APIView):
    def get(self, request):
        menu =Menu()
        optionsModbusMap =menu.setup_folder_path()
        print(optionsModbusMap[0])
        return JsonResponse({"modbus_map":optionsModbusMap[0]})
    @csrf_exempt  # Esto desactiva la verificación CSRF para esta vista
    def post(self,request):
        data = json.loads(request.body)
        url =data.get("selectedValue")
        path_modbus = "/FW/Modbus/modbusmaps"+"/"+url

        
        
        files_json = [archivo for archivo in os.listdir(path_modbus) if archivo.endswith('.json')]
        print(files_json)
        return JsonResponse({"data":files_json})