import configparser
import json
import os
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from utils.configfiles import ConfigFilePaths
from utils.menu import Menu
from utils.menu_single_device import SingleDeviceRead


config = configparser.ConfigParser(interpolation=None)
cf = ConfigFilePaths()
list_path_menu = cf.to_list()


class FormModbusReadRtu(APIView):
    """
    A class that handles HTTP PUT requests to update Modbus configuration data in a configuration file.

    This class is responsible for processing the incoming data (in JSON format), validating it, and updating the
    appropriate sections of a configuration file with the new values. If any required data is missing or invalid,
    the class returns an error message. Otherwise, it writes the updated configuration to the file.

    Methods:
    --------
    put(request):
        Handles PUT requests to update Modbus settings in the configuration file. It checks for valid data,
        updates the relevant sections of the configuration, and saves the changes to the file.

        The method also handles errors like invalid or missing data, as well as issues with file writing and JSON parsing.
    """
    def put(self, request):
        try:
            config.clear() 
            config.read(list_path_menu[6])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            name_section = f"Default"

            if not config.has_section(name_section):
                return JsonResponse({"message": f"Error: The device '{name_section}' do no exist"}, status=400)

            config.set(name_section, "mode_read ", str(data.get("typeComunication")))
            config.set(name_section, "max_attempts ", str(data.get("attempts")))
            config.set(name_section, "timeout_attempts ", str(data.get("timeout")))
            
            
            name_section = f"Configuration"
            
            if not config.has_section(name_section):
                return JsonResponse({"message": f"Error: The device '{name_section}' do no exist"}, status=400)

            config.set(name_section, "serial_port  ", str(data.get("portDevice")))
            config.set(name_section, "baudrate  ", str(data.get("baudrate")))
            config.set(name_section, "slave_id ", str(data.get("idSlave")))
            config.set(name_section, "modbus_function", str(data.get("modbus_function")))
            config.set(name_section, "address_init", str(data.get("initial_address")))
            config.set(name_section, "total_registers", str(data.get("total_registers")))
     

            with open(list_path_menu[6], "w") as configfile:
                config.write(configfile)
            device_read =  SingleDeviceRead(
                                            name_config = self.path_config_single
                                        )
            device_read.main()
            return JsonResponse({"message": "Data updated correctly"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Error parsing JSON data"}, status=400)
        except Exception as ex:
            return JsonResponse({"message": f"Error updating data: {ex}"}, status=400)
        
        
class FormModbusReadTCP(View):
    """
        Handles PUT requests to update the Modbus TCP configuration in a configuration file.

        This method parses the incoming JSON data, validates it, and updates the "Default" and "Configuration"
        sections of the configuration file. After the configuration update, it triggers the Modbus reading 
        process by invoking the `SingleDeviceRead.main()` method. It then returns a JSON response indicating the 
        success or failure of the update operation.

        Parameters:
        -----------
        request : HttpRequest
            The HTTP request containing the JSON body with the new Modbus TCP configuration.

        Returns:
        --------
        JsonResponse
            A JSON response indicating the success or failure of the update operation.
            - Status code 200 for success.
            - Status code 400 for errors such as invalid data or issues with the configuration file.
        """
    def put(self, request):
        try:
            config.clear() 
            config.read(list_path_menu[6])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)
            
            
            name_section = f"Default"

            if not config.has_section(name_section):
                return JsonResponse({"message": f"Error: The device '{name_section}' do no exist"}, status=400)

            config.set(name_section, "mode_read ", str(data.get("typeComunication")))
            config.set(name_section, "max_attempts ", str(data.get("attempts")))
            config.set(name_section, "timeout_attempts ", str(data.get("timeout")))
            
            
            name_section = f"Configuration"
            
            if not config.has_section(name_section):
                return JsonResponse({"message": f"Error: The device '{name_section}' do no exist"}, status=400)
            
            
            config.set(name_section, "port", str(data.get("port")))
            config.set(name_section, "host", str(data.get("host")))
            config.set(name_section, "slave_id ", str(data.get("idSlave")))
            config.set(name_section, "modbus_function", str(data.get("modbus_function")))
            config.set(name_section, "address_init", str(data.get("initial_address")))
            config.set(name_section, "total_registers", str(data.get("total_registers_rtu")))
     

            with open(list_path_menu[6], "w") as configfile:
                config.write(configfile)
            
            device_read =  SingleDeviceRead(
                                            name_config = self.path_config_single
                                        )
            device_read.main()

            return JsonResponse({"message": "Data updated correctly"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Error parsing JSON data"}, status=400)
        except Exception as ex:
            return JsonResponse({"message": f"Error updating data: {ex}"}, status=400)