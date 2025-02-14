import configparser
from django.http import JsonResponse
from django.views import View

from utils.configfiles import configfilepaths

config = configparser.ConfigParser()
cf = configfilepaths()
list_path_menu = cf.to_list()

class MeasureView(View):
    def get(self, request):
        try:
            config.read(list_path_menu[0])
            sample_data = {
                "zone": config.get('measurementmodbus', 'timezone'),
                "modbus": config.get('measurementmodbus','sampling_modbus'),
                "start": config.get('measurementmodbus', 'start_hour'),
                "stop": config.get('measurementmodbus', 'stop_hour'),
            }
            print("Hola")
            print(sample_data)
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataServer(View):
    def get(self, request):
        try:
            sample_data = {
                "server": config.get('server', 'server_type'),
                "neu_plus": config.get('server', 'id_device'),
                "telemetry": config.get('server', 'identify_id'),
                "mqtt": config.get('server', 'sampling_mqtt'),
                "storage": config.get('server', 'sampling_storage_plus'),
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataModes(View):
    def get(self, request):
        try:
            config.read(list_path_menu[0])
            limitation = 'No' if config.get('functioning', 'enable_active_limitation') == "False" else 'Yes'
            compensation = 'No' if config.get('functioning', 'enable_reactive_compensation') == "False" else 'Yes'
            sample_data = {
                "mode": config.get('functioning', 'work_mode'),
                "limitation": limitation,
                "compensation": compensation,
                "sampling_limitation": config.get('functioning', 'time_active_power'),
                "sampling_compensation": config.get('functioning', 'time_reactive_power'),
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataSettingDataBase(View):
    def get(self, request):
        try:
            config.read(list_path_menu[0])
            sample_data = {
                "day": config.get('database', 'old_days'),
                "await": config.get('database', 'await_to_while'),
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataSettingInterface(View):
    def get(self, request):
        try:
            sample_data = {
                "interface": config.get('internet_interfaces', 'internet_interface'),
                "connection": config.get('internet_interfaces', 'connection_name'),
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataLimitation(View):
    def get(self, request):
        try:
            config.read(list_path_menu[4])
            limitation = "Yes" if config.getboolean('Active', 'energy_meter_3p', fallback=False) else "No"
            sample_data = {
                "limitation": limitation,
                "meter_ids": config.get('Active', 'energy_meter_ids', fallback="1,2"),
                "inverter_ids": config.get('Active', 'inverter_ids', fallback="1,2"),
                "porcentage": config.getfloat('Active', 'active_power_percentage', fallback=0.02),
                "grid_min": config.getfloat('Active', 'active_power_grid_min', fallback=5.0),
                "grid_max": config.getfloat('Active', 'active_power_grid_max', fallback=10.0),
                "inverter_min": config.getint('Active', 'active_power_inv_min', fallback=0),
                "inverterMax": config.getint('Active', 'active_power_inv_max', fallback=1000),
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataCompensation(View):
    def get(self, request):
        try:
            config.read(list_path_menu[5])
            limitation = "Yes" if config.getboolean("Reactive", "reactive_power_limiter", fallback=False) else "No"
            sample_data = {
                "reactive_power": limitation,
                "meter_ids": config.get("Reactive", "energy_meter_ids", fallback="4"),
                "smart_logger": config.get("Reactive", "smartlogger_id", fallback="10"),
                "high": config.getfloat("Reactive", "reactive_power_percentage_high", fallback=0.40),
                "low": config.getfloat("Reactive", "reactive_power_percentage_low", fallback=0.30),
                "reactive": config.getint("Reactive", "reactive_offset", fallback=0),
                "active": config.getint("Reactive", "active_offset", fallback=0),
                "time": config.getfloat("Reactive", "time_active_power", fallback=0.1),
                "factor": config.getfloat("Reactive", "pf_min", fallback=0.91)
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

class FormDataBasePropierties(View):
    def get(self, request):
        try:
            config.read(list_path_menu[1])
            sample_data = {
                "host": config.get('DATABASE', 'host', fallback='localhost'),
                "port": config.get('DATABASE', 'port', fallback='27017'),
                "name": config.get('DATABASE', 'database', fallback='device_local_database'),
                "timeout": config.get('DATABASE', 'timeout', fallback='10'),
                "date": config.get('DATABASE', 'db_date_format', fallback='%%Y-%%m-%%d %%H:%%M:%%S')
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})


class FormDataSettingLogs(View):
    def get(self, request):
        try:
            config.read(list_path_menu[0])
            sample_data = {
                "level": config.get('DEFAULT', 'loglevel'),
                "stdout": config.get('DEFAULT', 'logstdout'),
                "file": config.get('DEFAULT', 'logfile'),
                "enable": config.get('DEFAULT', 'sampleslog'),
                "log_size": config.get('DEFAULT', 'max_size_bytes'),
                "backup": config.get('DEFAULT', 'backup_count'),


            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})



class FormDataModemChecker(View):
    def get(self, request):
        try:
            config.read(list_path_menu[3])
            sample_data = {
                "connection": config.get('MODEM_CHECKER', 'connection_name'),
                "attemts": config.get('MODEM_CHECKER', 'attempts_state'),
                

            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})


class FormDataSignalChecker(View):
    def get(self, request):
        try:
            config.read(list_path_menu[3])
            sample_data = {
                "onomondo": config.get('SIGNAL_CHECKER', 'min_quality_gsm'),
                "minimum": config.get('SIGNAL_CHECKER', 'min_quality_wifi'),
                

            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
class FormDataServerChecker(View):
    def get(self, request):
        try:
            config.read(list_path_menu[3])
            sample_data = {
                "requests": config.get('SERVER_CHECKER', 'max_attempts'),
                

            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})