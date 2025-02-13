import configparser
from django.http import JsonResponse
from django.views import View

from utils.configfiles import configfilepaths
# from EnrgUtilityManager.configfiles import configfilepaths


config = configparser.ConfigParser()
cf = configfilepaths()
list_path_menu = cf.to_list()
list_config=[]
# for i in range(len(list_path_menu)):
#             config = configparser.ConfigParser()
#             config.read(list_path_menu[i])
#             list_config.append(config)

class MeasureView(View):
    def get(self, request):
        config.read(list_path_menu[0])

        sample_data = {
            "zone": config.get('measurementmodbus', 'timezone'),
            "modbus": config.get('measurementmodbus'),
            "start": config.get('measurementmodbus', 'start_hour'),
            "stop": config.get('measurementmodbus', 'stop_hour'),
        }
        return JsonResponse(sample_data)

class FormDataServer(View):
    def get(self, request):
        sample_data = {
            "Server": config.get('server', 'server_type'),  # Puede ser "Telemetry", "Neu plus" o "All services"
            "neu_plus": config.get('server', 'id_device'),
            "telemetry": config.get('server', 'identify_id'),
            "mqtt": config.get('server', 'sampling_mqtt'),
            "storage": config.get('server', 'sampling_storage_plus'),
        }
        return JsonResponse(sample_data)
    
class FormDataModes(View):
    def get(self, request):
        config.read(list_path_menu[0])
        limitation='No'
        if config.get('functioning', 'enable_active_limitation') == "False":
            limitation='No'
        else:
             limitation='Yes'

        compensation='No'

        if config.get('functioning', 'enable_reactive_compensation') == "False":
            compensation='No'
        else:
             compensation='Yes'
        sample_data = {
             "mode": config.get('functioning', 'work_mode'),            # Valor de ejemplo para el modo
            "limitation": limitation,            # Opciones: "Yes" o "No"
            "compensation": compensation,           # Opciones: "Yes" o "No"
            "sampling_limitation": config.get('functioning', 'time_active_power'),    # Ejemplo: 5 segundos
            "sampling_compensation": config.get('functioning', 'time_reactive_power'), # Ejemplo: 10 segundos
        }
        return JsonResponse(sample_data)

class FormDataSettingDataBase(View):
    def get(self,request):
        config.read(list_path_menu[0])
        sample_data = {
            "day":config.get('database', 'old_days'),
            "await":config.get('database', 'await_to_while'),
        }
        return JsonResponse(sample_data)
    
class FormDataSettingInterface(View):
    def get(self,request):
        sample_data = {
            "interface":config.get('internet_interfaces', 'internet_interface'),
            "connection":config.get('internet_interfaces', 'connection_name'),
        }
        return JsonResponse(sample_data)

class FormDataLimitation(View):
    def get(self,request):
        config.read(list_path_menu[4])
        limitation="No"
        if config.getboolean('Active', 'energy_meter_3p', fallback=False)==True:
            limitation="Yes"
        else:
            limitation="No" 

        sample_data= {
            "limitation":limitation,
            "meter_ids":config.get('Active', 'energy_meter_ids', fallback="1,2"),
            "inverter_ids":config.get('Active', 'inverter_ids', fallback="1,2"),
            "porcentage":str(config.getfloat('Active', 'active_power_percentage', fallback=0.02)),
            "grid_min":str(config.getfloat('Active', 'active_power_grid_min', fallback=5.0)),
            "grid_max":str(config.getfloat('Active', 'active_power_grid_max', fallback=10.0)),
            "inverter_min":str(config.getint('Active', 'active_power_inv_min', fallback=0)),
            "inverterMax":str(config.getint('Active', 'active_power_inv_max', fallback=1000)),

        }
        return JsonResponse(sample_data)

class FormDataCompensation(View):
    config.read(list_path_menu[5])

    def get(self,request):
        limitation="No"
        if config.getboolean(
                    "Reactive", "reactive_power_limiter", fallback=False
                ) == True:
            limitation="Yes"
        else:
            limitation="No"
        sample_data= {
            "reactive_power":limitation,
            "meter_ids":config.get(
                    "Reactive", "energy_meter_ids", fallback="4"
                ),
            "smart_logger":config.get(
                    "Reactive", "smartlogger_id", fallback="10"
                ),
            "high":config.getfloat(
                    "Reactive", "reactive_power_percentage_high", fallback=0.40
                ),
            "low":config.getfloat(
                    "Reactive", "reactive_power_percentage_low", fallback=0.30
                ),
            "reactive":config.getint(
                    "Reactive", "reactive_offset", fallback=0
                ),
            "active":config.getint(
                    "Reactive", "active_offset", fallback=0
                ),
            "time":config.getfloat(
                    "Reactive", "time_active_power", fallback=0.1
                ),
            "factor":config.getfloat("Reactive", "pf_min", fallback=0.91)
        }
        return JsonResponse(sample_data)
    


class FormDataBasePropierties(View):
    def get(self,request):
        config.read(list_path_menu[1])
        sample_data= {
            "host":config.get('DATABASE', 'host', fallback='localhost'),
            "port":config.get('DATABASE', 'port', fallback='27017'),
            "name":config.get('DATABASE', 'database', fallback='device_local_database'),
            "timeout":config.get('DATABASE', 'timeout', fallback='10'),
            "date":config.get('DATABASE', 'db_date_format', fallback='%%Y-%%m-%%d %%H:%%M:%%S')
            

        }
        return JsonResponse(sample_data)

