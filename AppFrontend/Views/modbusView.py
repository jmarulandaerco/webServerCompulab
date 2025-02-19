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
        
    def put(self, request):
        
        try:
            
            config.read(list_path_menu[2])

            data = json.loads(request.body)
            devices = data.get("selectedDevices")
            
            config.set("Default", "devices_config", ",".join(devices))

           
                                
            with open(list_path_menu[2], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 



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
    

class FormModbusAddDeviceRtu(View):
    def post(self,request):
        
        
        try:
            data = json.loads(request.body)
            print("Hola")
            print(data)
            config.read(list_path_menu[2])
            new_name_device="Modbus-RTU-"+data.get("nameDevice")
            
            current_devices = self.config.get("Default", "devices_config")
            current_sections = self.config.sections()
            if new_name_device in current_sections:
                return JsonResponse({"message": f"Error el Dispositivo ya existe, {e}"}, status=400)
            updated_device_list = (
                            current_devices + "," + new_name_device
                            if current_devices
                            else new_name_device
                        )

            config.set(
                            "Default", "devices_config", updated_device_list
                        )
            
            with open(list_path_menu[2], "w") as configfile:
                config.write(configfile)
            
            print("/FW/Modbus/modbusmaps/{}/{}".format(data.get("modbus_map_folder"), data.get("modbus_map_json")))
            
            config[new_name_device] = {
                        "serial_port": data.get("portDevice"),
                        "baudrate": data.get("baudrate"),
                        "slave_id_start": data.get("initial"),
                        "slave_id_end": data.get("end"),
                        "modbus_function": data.get("modbus_function"),
                        "address_init": data.get("initial_address"),
                        "total_registers": data.get("total_registers"),
                        "protocol_type": "DeviceProtocol.MODBUS_RTU_MASTER",
                        "modbus_map_file": f"/FW/Modbus/modbusmaps/{data.get('modbus_map_folder')}/{data.get('modbus_map_json')}",
                        "modbus_mode": data.get("modbus_mode"),
                        "device_type": data.get("device_type"),
                        "address_offset": 0,
                        "storage_db": data.get("save_db"),
                        "send_server": data.get("server_send"),
                        "attempts_wait": 0.2,
                    }
            with open(list_path_menu[2]) as configfile:
                    config.write(configfile)
            return JsonResponse({"message": "Datos actualizados"}, status=200)
        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 