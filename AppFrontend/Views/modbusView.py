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
        try:
            config.read(list_path_menu[2])
            sample_data = {
                "debug": config.get('Default', 'log_debug', fallback='INFO'),
                "attempts":config.get('Default', 'max_attempts', fallback='3'),
                "timeout": config.get('Default', 'timeout_attempts', fallback='1'),
            }
            return JsonResponse(sample_data)
        except Exception as ex:
            return JsonResponse({"message": f"Error updating data, {ex}"}, status=400)

    def put(self, request):
        try:
            config.read(list_path_menu[2])
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            config.set('Default', 'log_debug', str(data.get("log_debug")))
            config.set('Default', 'max_attempts', str(data.get("max_attempts")))
            config.set('Default', 'timeout_attempts', str(data.get("timeout_attempts")))
            
            with open(list_path_menu[2], 'w') as configfile:
                config.write(configfile)
            
            return JsonResponse({"message": "Updated data"})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Error updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error updating data, {e}"}, status=400)

class FormModbusDevicesView(View):
    def get(self, request):
        device_param = request.GET.get('device', '') 

        if not device_param: 
            return HttpResponseNotFound("Error: A device was not specified.")

        config.read(list_path_menu[2])
        menu = Menu()
        a = menu.setup_folder_path()
  
        current_devices = config.sections()
        if "Default" in current_devices:
            current_devices.remove("Default")

        enabled_devices = config.get("Default", "devices_config", fallback="").split(",")

        listDevices = current_devices
        listSelectedDevices = enabled_devices

      

        template_name = f'home/content/form/modbus/{device_param}.html'

        try:
             return render(request, template_name, {
            'listDevices': listDevices,
            'listSelectedDevices': listSelectedDevices
        })
        except:
            return HttpResponseNotFound(f"Error: The template {template_name} does not exist.")
        
    def put(self, request):
        
        try:
            
            config.read(list_path_menu[2])

            data = json.loads(request.body)
            devices = data.get("selectedDevices")
            
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            
            config.set("Default", "devices_config", ",".join(devices))

           
                                
            with open(list_path_menu[2], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Updated data."}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error updating data"}, status=400)    
        except Exception as e:
            return JsonResponse({"message": f"Error updating data, {e}"}, status=400) 



class FormModbusGetDevicesView(APIView):
    def get(self, request):
        try:
            menu =Menu()
            optionsModbusMap =menu.setup_folder_path()
            return JsonResponse({"modbus_map":optionsModbusMap[0]})
        except Exception as ex:
            return JsonResponse({"message": f"Error in obtaining data, {ex}"}, status=400) 

    @csrf_exempt 
    def post(self,request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            url =data.get("selectedValue")
            path_modbus = "/FW/Modbus/modbusmaps"+"/"+url

            
            
            files_json = [archivo for archivo in os.listdir(path_modbus) if archivo.endswith('.json')]
            return JsonResponse({"data":files_json})
        except Exception as ex:
            return JsonResponse({"message": f"Error saving data, {ex}"}, status=400) 

    
    @csrf_exempt
    def delete(self, request):
        try:
            config.read(list_path_menu[2])
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
         
            
            filename = data.get("device")

            enabled_devices = config.get("Default", "devices_config", fallback="").split(",")

            enabled_devices = [dev.strip() for dev in enabled_devices if dev.strip()]

            if filename  in enabled_devices:
               

                enabled_devices.remove(filename)

                new_list_devices = ','.join(enabled_devices)
                config.set('Default', 'devices_config', new_list_devices)

            if config.has_section(filename):
                config.remove_section(filename)

            with open(list_path_menu[2], 'w') as configfile:
                config.write(configfile)

            return JsonResponse({"message": "Device successfully removed."}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=400)

class FormModbusAddDeviceRtu(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            config.read(list_path_menu[2])
            
            new_name_device="Modbus-RTU-"+data.get("nameDevice")
            
            current_devices =config.get("Default", "devices_config")
            current_sections = config.sections()
            if new_name_device in current_sections:
                return JsonResponse({"message": f"Error Device already exists"}, status=400)
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

            return JsonResponse({"message": "Updated data"}, status=200)
        
        except Exception as ex:
            return JsonResponse({"message": f'Error updating datas, {ex}'}, status=400)
    
    def put(self, request):
        try:
            config.read(list_path_menu[2])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            nombre_seccion = f"Modbus-RTU-{data.get('nameDevice')}"

            if not config.has_section(nombre_seccion):
                return JsonResponse({"message": f"Error: The device '{nombre_seccion}' do no exist"}, status=400)

            config.set(nombre_seccion, "serial_port", str(data.get("portDevice")))
            config.set(nombre_seccion, "baudrate", str(data.get("baudrate")))
            config.set(nombre_seccion, "slave_id_start", str(data.get("initial")))
            config.set(nombre_seccion, "slave_id_end", str(data.get("end")))
            config.set(nombre_seccion, "modbus_function", str(data.get("modbus_function")))
            config.set(nombre_seccion, "address_init", str(data.get("initial_address")))
            config.set(nombre_seccion, "total_registers", str(data.get("total_registers")))
            config.set(nombre_seccion, "protocol_type", "DeviceProtocol.MODBUS_RTU_MASTER")
            config.set(nombre_seccion, "modbus_map_file", f"/FW/Modbus/modbusmaps/{str(data.get('modbus_map_folder'))}/{str(data.get('modbus_map_json'))}")
            config.set(nombre_seccion, "modbus_mode", str(data.get("modbus_mode")))
            config.set(nombre_seccion, "device_type", str(data.get("device_type")))
            config.set(nombre_seccion, "address_offset", "0")
            config.set(nombre_seccion, "storage_db", str(data.get("save_db")))
            config.set(nombre_seccion, "send_server", str(data.get("server_send")))
            config.set(nombre_seccion, "attempts_wait", "0")

            with open(list_path_menu[2], "w") as configfile:
                config.write(configfile)

            return JsonResponse({"message": "Data updated correctly"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Error parsing JSON data"}, status=400)
        except Exception as ex:
            return JsonResponse({"message": f"Error updating data: {ex}"}, status=400)
            

class FormModbusAddDeviceTcp(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            config.read(list_path_menu[2])
            
            new_name_device="Modbus-TCP-"+data.get("nameDevice")
            
            current_devices =config.get("Default", "devices_config")
            current_sections = config.sections()
            if new_name_device in current_sections:
                return JsonResponse({"message": f"Error Device already exists"}, status=400)
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

            return JsonResponse({"message": "Updated data"}, status=200)
        
        except Exception as ex:
            return JsonResponse({"message": f'Error updating data, {ex}'}, status=400)
    def put(self, request):
        try:
            data = json.loads(request.body)
            config.read(list_path_menu[2])
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            device_name = f"Modbus-TCP-{data.get('nameDevice')}"

            if not config.has_section(device_name):
                return JsonResponse({"message": f"Error: The device '{device_name}' does not exist"}, status=400)

            offset = int(data.get("offset", 0))
            attempts_wait = 0.2 if offset > 0 else 0

            config.set(device_name, "host_ip", str(data.get("ip_device")))
            config.set(device_name, "port_ip", str(data.get("port_device")))
            config.set(device_name, "slave_id_start", str(data.get("initial")))
            config.set(device_name, "slave_id_end", str(data.get("end")))
            config.set(device_name, "modbus_function", str(data.get("modbus_function")))
            config.set(device_name, "address_init", str(data.get("initial_address")))
            config.set(device_name, "total_registers", str(data.get("total_registers")))
            config.set(device_name, "protocol_type", "DeviceProtocol.MODBUS_TCP")
            config.set(device_name, "modbus_map_file", f"/FW/Modbus/modbusmaps/{data.get('modbus_map_folder')}/{data.get('modbus_map_json')}")
            config.set(device_name, "modbus_mode", str(data.get("modbus_mode")))
            config.set(device_name, "device_type", str(data.get("device_type")))
            config.set(device_name, "address_offset", str(offset))
            config.set(device_name, "storage_db", str(data.get("save_db")))
            config.set(device_name, "send_server", str(data.get("server_send")))
            config.set(device_name, "attempts_wait", str(attempts_wait))

            with open(list_path_menu[2], "w") as configfile:
                config.write(configfile)

            return JsonResponse({"message": "Data updated correctly"}, status=200)

        except Exception as ex:
            return JsonResponse({"message": f"Error updating data: {ex}"}, status=400)   

class FormModbusDeviceRtuView(View):
    def get(self, request):
        try:
            device_param = request.GET.get('device', '')  
            if not device_param:
                return JsonResponse({"message": "The ‘device’ parameter is required."}, status=400)

            config.read(list_path_menu[2])

            if device_param not in config:
                return JsonResponse({"message": f"The section '{device_param}' does not exist in the configuration."}, status=400)

            data = config[device_param]
            path = str(data.get("modbus_map_file", ""))
            parts = path.split("/")
            map_folder = parts[-2]  
            map_json = parts[-1]    


            data.get("device_type", "")
 
            
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
            return JsonResponse({"message": f"Error updating data: {str(ex)}"}, status=400)