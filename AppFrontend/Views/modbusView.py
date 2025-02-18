import configparser
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

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
    # def get(self,request):
    #     config.read(list_path_menu[2])
        
    #     current_devices = config.sections()
    #     current_devices.remove("Default")
    #     enabled_devices = config.get(
    #             "Default", "devices_config", fallback=""
    #         ).split(",")
    #     print(current_devices)
    #     print(enabled_devices)
    #     return JsonResponse({"listDevices":current_devices, "listSelectedDevices":enabled_devices})

    
    
    def get(self, request):
        config.read(list_path_menu[2])
        menu =Menu()
        a =menu.setup_folder_path()
        print("Holiii")
        print(a)
        current_devices = config.sections()
        current_devices.remove("Default")
        enabled_devices = config.get(
                "Default", "devices_config", fallback=""
            ).split(",")
        
        listDevices = current_devices
        listSelectedDevices = enabled_devices
        print(listDevices)
        print(listSelectedDevices)
        return render(request, 'home/content/form/seeDevices.html', {
            'listDevices': listDevices,
            'listSelectedDevices': listSelectedDevices
        })