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
    
    @csrf_exempt
    def delete(self, request):
        try:
            config.read(list_path_menu[2])
            data = json.loads(request.body)
            filename = data.get("device")
            enabled_devices = config.get("Default", "devices_config", fallback="").split(",")
            
            if filename not in enabled_devices:
                return JsonResponse({"message": "El dispositivo no existe."}, status=400)
            
            index = enabled_devices.index(filename)
            current_devices = config.sections()
            current_devices.remove('Default')
            delete_device=current_devices[index]
            current_devices.remove(delete_device)
            new_list_devices = ','.join(current_devices)
            config.set('Default', 'devices_config', new_list_devices)
            if config.has_section(delete_device):
                config.remove_section(delete_device)

            with open(list_path_menu[2], 'w') as configfile:
                config.write(configfile)

            return JsonResponse({"message": "Archivo eliminado correctamente.", "index": index}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=500)



class FormModbusAddDeviceRtu(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            
            config.read(list_path_menu[2])
            
            new_name_device="Modbus-RTU-"+data.get("nameDevice")
            
            current_devices =config.get("Default", "devices_config")
            current_sections = config.sections()
            if new_name_device in current_sections:
                return JsonResponse({"message": f"Error el Dispositivo ya existe"}, status=400)
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
            
            print("/FW/Modbus/modbusmaps/{}/{}".format(str(data.get("modbus_map_folder")), str(data.get("modbus_map_json"))))
            
            config[new_name_device] = {
                        "serial_port": str(data.get("portDevice")),
                        "baudrate": str(data.get("baudrate")),
                        "slave_id_start": str(data.get("initial")),
                        "slave_id_end": str(data.get("end")),
                        "modbus_function": str(data.get("modbus_function")),
                        "address_init": str(data.get("initial_address")),
                        "total_registers": str(data.get("total_registers")),
                        "protocol_type": "DeviceProtocol.MODBUS_RTU_MASTER",
                        "modbus_map_file": f"/FW/Modbus/modbusmaps/{str(data.get('modbus_map_folder'))}/{str(data.get('modbus_map_json'))}",
                        "modbus_mode": str(data.get("modbus_mode")),
                        "device_type": str(data.get("device_type")),
                        "address_offset": str(0),
                        "storage_db": str(data.get("save_db")),
                        "send_server": str(data.get("server_send")),
                        "attempts_wait": str(0),
                    }
            with open(list_path_menu[2], "w") as configfile:
                config.write(configfile)

            return JsonResponse({"message": "Datos actualizados"}, status=200)
        
        except Exception as ex:
            print(ex)
            return JsonResponse({"message": f'Error al actualizar los datos, {ex}'}, status=400)
        
        

class FormModbusAddDeviceTcp(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            
            config.read(list_path_menu[2])
            
            new_name_device="Modbus-TCP-"+data.get("nameDevice")
            
            current_devices =config.get("Default", "devices_config")
            current_sections = config.sections()
            if new_name_device in current_sections:
                return JsonResponse({"message": f"Error el Dispositivo ya existe"}, status=400)
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
            
            print("/FW/Modbus/modbusmaps/{}/{}".format(str(data.get("modbus_map_folder")), str(data.get("modbus_map_json"))))
            attempts_wait=0
            if int(data.get("offset")) > 0:
                    attempts_wait = 0.2
            else:
                    attempts_wait = 0
            config[new_name_device] = {
                        "host_ip": str(data.get("ip_device")),
                        "port_ip": str(data.get("port_device")),
                        "slave_id_start": str(data.get("initial")),
                        "slave_id_end": str(data.get("end")),
                        "modbus_function": str(data.get("modbus_function")),
                        "address_init": str(data.get("initial_address")),
                        "total_registers": str(data.get("total_registers")),
                        "protocol_type": "DeviceProtocol.MODBUS_TCP",
                        "modbus_map_file": f"/FW/Modbus/modbusmaps/{str(data.get('modbus_map_folder'))}/{str(data.get('modbus_map_json'))}",
                        "modbus_mode": str(data.get("modbus_mode")),
                        "device_type": str(data.get("device_type")),
                        "address_offset": str(data.get("offset")),
                        "storage_db": str(data.get("save_db")),
                        "send_server": str(data.get("server_send")),
                        "attempts_wait": str(attempts_wait),
                    }
            
          
            with open(list_path_menu[2], "w") as configfile:
                config.write(configfile)

            return JsonResponse({"message": "Datos actualizados"}, status=200)
        
        except Exception as ex:
            print(ex)
            return JsonResponse({"message": f'Error al actualizar los datos, {ex}'}, status=400)
        

class FormModbusDeviceRtuView(View):
    def get(self, request):
        try:
            device_param = request.GET.get('device', '')  

            config.read(list_path_menu[2])
            
            data = config[device_param]
            
            path = "valores/FW/Modbus/modbusmaps/HUAWEI/HUAWEI_INV.json"

            # Dividir el string por "/"
            parts = path.split("/")

            # Obtener los últimos dos elementos
            last_two_elements = parts[-2:]  

            map_forder = last_two_elements[0]  # "HUAWEI"
            map_json = last_two_elements[1] # "HUAWEI_INV.json"
            print("Esto esta cuca")
            print(data)
            information={
                "nameRtu": device_param,
                "portRtu":data.serial_port,
                "baudrateRtu":data.baudrate,
                "initialRtu":data.slave_id_start,
                "endRtu":data.slave_id_end,
                "modbus_function_rtu":data.address_init,
                "initial_address_rtudata":data.total_registers,
                "total_registers_rtu":data.modbus_map_file,
                "modbus_map_folder_rtu":map_forder,
                "modbus_map_json_rtu":map_json,
                "modbus_mode_rtu":data.address_offset,
                "device_type_rtu":data.storage_db,
                "save_db_rtu":data.send_server,
                "server_send_rtu":data.attempts_wait
            }
            
            return JsonResponse(information)
        except Exception as ex:
            return JsonResponse({"message": f'Error al actualizar los datos, {ex}'}, status=400)
        
    