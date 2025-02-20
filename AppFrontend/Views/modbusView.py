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
        config.read(list_path_menu[2])
        sample_data = {
            "debug": config.get('Default', 'log_debug', fallback='INFO'),
            "attempts":config.get('Default', 'max_attempts', fallback='3'),
            "timeout": config.get('Default', 'timeout_attempts', fallback='1'),
        }
        
        
        
        
        return JsonResponse(sample_data)
    
    def put(self, request):
        try:
            config.read(list_path_menu[2])
            data = json.loads(request.body)
            print(data)
            
            # Convertir los valores a cadenas antes de establecerlos
            config.set('Default', 'log_debug', str(data.get("log_debug")))
            config.set('Default', 'max_attempts', str(data.get("max_attempts")))
            config.set('Default', 'timeout_attempts', str(data.get("timeout_attempts")))
            
            with open(list_path_menu[2], 'w') as configfile:
                config.write(configfile)
            
            return JsonResponse({"message": "Datos actualizados"})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400)

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
            print(device_param)
            # Validar que el parámetro no está vacío
            if not device_param:
                return JsonResponse({"message": "El parámetro 'device' es requerido."}, status=400)

            # Crear y leer el archivo de configuración
            config.read(list_path_menu[2])

            # Verificar si la sección existe
            if device_param not in config:
                return JsonResponse({"message": f"La sección '{device_param}' no existe en la configuración."}, status=400)

            # Obtener datos de la sección de configuración
            data = config[device_param]
            # Ruta del archivo Modbus
            path = str(data.get("modbus_map_file", ""))
            parts = path.split("/")
            map_folder = parts[-2]  # "HUAWEI"
            map_json = parts[-1]    # "HUAWEI_INV.json"

            # Crear diccionario con la información
            print("Information")
            data.get("device_type", "")
            print(map_folder)
            print(map_json)
            print(str(data.get("modbus_map_file", ""))),
            
            if "RTU" in device_param:
                information = {
                    "nameRtu": device_param.replace("Modbus-RTU-", ""),
                    "portRtu": data.get("serial_port", ""),
                    "baudrateRtu": data.get("baudrate", ""),
                    "initialRtu": data.get("slave_id_start", ""),
                    "endRtu": data.get("slave_id_end", ""),
                    "modbus_function_rtu": data.get("modbus_function", ""),
                    "initial_address_rtu": data.get("address_init", ""),
                    "total_registers_rtu": data.get("total_registers", ""),
                    "modbus_map_folder_rtu": str(map_folder),
                    "modbus_map_json_rtu": str(map_json),
                    "modbus_mode_rtu": data.get("modbus_mode", ""),
                    "device_type_rtu": data.get("device_type", ""),
                    "save_db_rtu": data.get("storage_db", ""),
                    "server_send_rtu": data.get("send_server", "")
                }
            else:
                print("123")
                print(data.get("device_type", ""))
                information = {
                    "nameTcp": device_param.replace("Modbus-TCP-", ""),
                    "ip_device_tcp": data.get("host_ip", ""),
                    "port_device_tcp": data.get("port_ip", ""),
                    "offset_tcp": data.get("address_offset", ""),
                    "initial_tcp": data.get("slave_id_start", ""),
                    "end_tcp": data.get("slave_id_end", ""),
                    "modbus_function_tcp": data.get("modbus_function", ""),
                    "initial_address_tcp": data.get("address_init", ""),
                    "total_registers_tcp": data.get("total_registers", ""),
                    "modbus_map_folder_tcp": str(map_folder),
                    "modbus_map_json_tcp": str(map_json),
                    "modbus_mod_tcp": data.get("modbus_mode", ""),
                    "device_type_tcp": data.get("device_type", ""),
                    "save_db_tcp": data.get("storage_db", ""),
                    "server_send_tcp": data.get("send_server", "")
                }
            return JsonResponse(information)

        except Exception as ex:
            return JsonResponse({"message": f"Error al actualizar los datos: {str(ex)}"}, status=400)