import configparser
from django.http import JsonResponse
from django.views import View

from utils.configfiles import configfilepaths


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
    def get(self,request):
        config.read(list_path_menu[2])
        
        current_devices = config.sections()
        current_devices.remove("Default")
        enabled_devices = config.get(
                "Default", "devices_config", fallback=""
            ).split(",")
        print(current_devices)
        print(enabled_devices)
        return JsonResponse({"prueba1":current_devices, "prueba2":enabled_devices})

        