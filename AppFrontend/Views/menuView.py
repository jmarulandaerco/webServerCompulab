import configparser
import json
from django.http import JsonResponse
from django.views import View

from utils.configfiles import configfilepaths
from utils.menu import Menu

config = configparser.ConfigParser(interpolation=None)
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
            
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    def put(self, request):
        
        try:
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            zone = data.get("zone")
            modbus = data.get("modbus")
            start = data.get("start")
            stop = data.get("stop")

            config.set(
                                "measurementmodbus", "timezone", zone
                            )
            config.set(
                                "measurementmodbus",
                                "sampling_modbus",
                                modbus,
                            )
            config.set(
                                "measurementmodbus", "start_hour", start
                            )
            config.set(
                                "measurementmodbus", "stop_hour", stop
                            )
            
            with open(list_path_menu[0], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 

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
        
    def put(self, request):
        
        try:
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            server = data.get("server")
            neu_plus = data.get("neu_plus")
            telemetry = data.get("telemetry")
            mqtt = data.get("mqtt")
            storage = data.get("storage")


            config.set("server", "server_type", server)
            config.set("server", "id_device", neu_plus)
            config.set(
                                    "server", "identify_id", telemetry
                                )
            config.set(
                                    "server", "sampling_mqtt", mqtt
                                )
            config.set(
                                    "server",
                                    "sampling_storage_plus",
                                    storage,
                                )
            with open(list_path_menu[0], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 

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
    def put(self, request):
        
        try:
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            mode = data.get("mode")
            limitation = data.get("limitation")
            compensation = data.get("compensation")
            sampling_limitation = data.get("sampling_limitation")
            sampling_compensation = data.get("sampling_compensation")
            
            config.set("functioning", "work_mode", mode)
            if limitation == "Yes":
                config.set(
                                "functioning",
                                "enable_active_limitation",
                                str(True),
                            )
            else:
                config.set(
                                "functioning",
                                "enable_active_limitation",
                                str(False),
                            )
                
            if compensation=="Yes":
                config.set(
                                "functioning",
                                "enable_reactive_compensation",
                                str(True),
                            )   
            else:
                config.set(
                                "functioning",
                                "enable_reactive_compensation",
                                str(False),
                            ) 

            config.set(
                                "functioning",
                                "time_active_power",
                                sampling_limitation,
                            )  
            config.set(
                                "functioning",
                                "time_reactive_power",
                                sampling_compensation,
                            )
            with open(list_path_menu[0], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 
class FormDataSettingDataBase(View):
    def get(self, request):
        try:
            config.read(list_path_menu[0])
            sample_data = {
                "day": config.get('database', 'old_days'),
                "awaitTime": config.get('database', 'await_to_while'),
            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    def put(self, request):
        
        try:
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            day = data.get("day")
            awaitTime = data.get("awaitTime")
           


            config.set("database", "old_days", day)
            config.set(
                                "database", "await_to_while", awaitTime
                            )
            
                                
            with open(list_path_menu[0], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 

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

    def put(self, request):
        
        try:
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            interface = data.get("interface")
            connection = data.get("connection")
           


            config.set(
                                "internet_interfaces",
                                "internet_interface",
                                interface,
                            )
            config.set(
                                "internet_interfaces",
                                "connection_name",
                                connection,
                            )
            
                                
            with open(list_path_menu[0], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 
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
        
    def put(self, request):
        
        try:
            config.read(list_path_menu[4])

            data = json.loads(request.body)

            selectedValue = data.get("selectedValue")
            meter_ids = data.get("meter_ids")
            inverter_ids = data.get("inverter_ids")
            porcentage = data.get("porcentage")
            grid_min = data.get("grid_min")
            grid_max = data.get("grid_max")
            inverter_min = data.get("inverter_min")
            inverterMax = data.get("inverterMax")
            
            if selectedValue == "Yes":
                config.set('Active', 'energy_meter_3p', str(True))

            else:
               config.set('Active', 'energy_meter_3p', str(False))
            
            config.set('Active', 'energy_meter_ids', meter_ids)

            config.set('Active', 'inverter_ids', inverter_ids)
            config.set('Active', 'active_power_percentage', porcentage)
            config.set('Active', 'active_power_grid_min', grid_min)
            config.set('Active', 'active_power_grid_max', grid_max)
            config.set('Active', 'active_power_inv_min', inverter_min)
            config.set('Active', 'active_power_inv_max', inverterMax)
            
           
            with open(list_path_menu[4], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 

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
        
    def put(self, request):
        
        try:
            config.read(list_path_menu[5])

            data = json.loads(request.body)

            selectedValue = data.get("selectedValue")
            meter_ids = data.get("meter_ids")
            smart_logger = data.get("smart_logger")
            high = data.get("high")
            low = data.get("low")
            reactive = data.get("reactive")
            active = data.get("active")
            time = data.get("time")
            factor = data.get("factor")
            
            if selectedValue == "Yes":
                config.set(
                            "Reactive", "reactive_power_limiter", str(True)
                        )

            else:
               config.set(
                            "Reactive", "reactive_power_limiter", str(False)
                        )
            
            config.set("Reactive", "energy_meter_ids", meter_ids)
            config.set(
                                "Reactive", "smartlogger_id", smart_logger
                            )
            config.set(
                                "Reactive",
                                "reactive_power_percentage_high",
                                high,
                            )
            config.set(
                                "Reactive",
                                "reactive_power_percentage_low",
                                low,
                            )
                            
            config.set(
                                "Reactive", "reactive_offset", reactive
                            )
            
            config.set(
                                "Reactive", "active_offset", active
                            )
            
            config.set(
                                "Reactive", "time_active_power", time
                            )
            config.set("Reactive", "pf_min", factor)
            with open(list_path_menu[5], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 

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
        
    def put(self, request):
        
        try:
            config.read(list_path_menu[1])

            data = json.loads(request.body)

            host = data.get("host")
            port = data.get("port")
            name = data.get("name")
            timeout = data.get("timeout")
            date = data.get("date")

            config.set("DATABASE", "host", host)
            config.set("DATABASE", "port", port)
            config.set("DATABASE", "database", name)
            config.set("DATABASE", "timeout", timeout)
            config.set("DATABASE", "db_date_format", date)
            
            with open(list_path_menu[1], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 


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
    def put(self, request):
        
        try:
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            level = data.get("level")
            stdout = data.get("stdout")
            file = data.get("file")
            enable = data.get("enable")
            log_size = data.get("log_size")
            backup = data.get("backup")


            config.set("DEFAULT", "loglevel", level)
           
            config.set("DEFAULT", "logstdout", stdout) 

            config.set("DEFAULT", "logfile", file)
            config.set("DEFAULT", "sampleslog", enable)
            config.set("DEFAULT", "max_size_bytes", log_size)
            config.set("DEFAULT", "backup_count", backup)
            with open(list_path_menu[0], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 



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

    def put(self, request):
        try:
            data = json.loads(request.body)
            config.read(list_path_menu[3])

            connection = data.get("connection")
            attemts = data.get("attemts")
            config.set(
                                'MODEM_CHECKER', 'connection_name', connection
                            )
            config.set(
                                'MODEM_CHECKER', 'attempts_state', attemts,
                            )
            
            with open(list_path_menu[3], "w") as configfileChecked:
               config.write(configfileChecked)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400) 
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
        
    def put(self, request):
        try:
            data = json.loads(request.body)
            config.read(list_path_menu[3])

            onomondo = data.get("onomondo")
            minimum = data.get("minimum")
            config.set(
                                'SIGNAL_CHECKER', 'min_quality_gsm', onomondo
                            )
            config.set(
                                "SIGNAL_CHECKER", "min_quality_wifi", minimum,
                            )
            with open(list_path_menu[3], "w") as configfile:
               config.write(configfile)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400)

    
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
        
    def put(self, request):
        try:
            config.read(list_path_menu[3])

            data = json.loads(request.body)

            requests = data.get("requests")
            config.set(
                                'SERVER_CHECKER', 'max_attempts', requests,
                            )
            with open(list_path_menu[3], "w") as configfile:
               config.write(configfile)
            return JsonResponse({"message": "Datos actualizados"}, status=200)

        except json.JSONDecodeError:
            
            return JsonResponse({"message": "Error al actualizar los datos"}, status=400)    
        except Exception as e:
            print(e)
            return JsonResponse({"message": f"Error al actualizar los datos, {e}"}, status=400)
        
        