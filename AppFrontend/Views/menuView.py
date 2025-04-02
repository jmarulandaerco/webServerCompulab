import configparser
import json
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView


from utils.configfiles import ConfigFilePaths
from utils.menu import Menu

config = configparser.ConfigParser(interpolation=None)
cf = ConfigFilePaths()
list_path_menu = cf.to_list()


class MeasureView(View):
    """
    View class for retrieving and updating measurement-related configuration settings.

    This view provides GET and PUT endpoints to manage measurement configuration parameters.
    The GET method retrieves the current measurement settings, including timezone, Modbus sampling,
    and start/stop hours. The PUT method updates these settings based on a JSON payload received in the
    request, writing the changes back to the configuration file.

    Methods:
    --------
    get(request):
        Retrieves the current measurement configuration settings from the configuration storage.

    put(request):
        Updates the measurement configuration settings using the data provided in the JSON payload.
    """

    def get(self, request):
        try:
            config.clear()
            config.read(list_path_menu[0])
            sample_data = {
                "zone": config.get('measurementmodbus', 'timezone'),
                "modbus": config.get('measurementmodbus', 'sampling_modbus'),
                "start": config.get('measurementmodbus', 'start_hour'),
                "stop": config.get('measurementmodbus', 'stop_hour'),
            }

            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    def put(self, request):

        try:
            config.clear()
            config.read(list_path_menu[0])

            data = json.loads(request.body)

            if any(value is None or value == '' for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)

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
            return JsonResponse({"message": "Updated data"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error updating data, {e}"}, status=400)


class FormDataServer(View):
    """
    View class for retrieving and updating server configuration settings.

    This view provides GET and PUT endpoints to manage server-related configuration parameters.
    The GET method retrieves the current server settings, including server type, device ID, telemetry
    identifier, MQTT sampling, and storage sampling values. The PUT method updates these settings based
    on a JSON payload received in the request, writing the changes back to the configuration file.

    Methods:
    --------
    get(request):
        Retrieves the current server configuration settings from the configuration storage.

    put(request):
        Updates the server configuration settings using the data provided in the JSON payload.
    """

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
            config.clear()
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)

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
            return JsonResponse({"message": "Updated data"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error updating data, {e}"}, status=400)


class FormDataModes(View):
    """
    View class for retrieving and updating the operational modes of the system.

    This view handles GET and PUT requests to manage the system's functioning modes,
    including work mode, active limitation, reactive compensation, and their associated
    sampling times. The GET method retrieves the current settings from a configuration file,
    converting boolean settings for active limitation and reactive compensation into "Yes" or "No" strings.
    The PUT method accepts a JSON payload to update these settings in the configuration file.

    Methods:
    --------
    get(request):
        Retrieves the current operational mode settings from the configuration file.

    put(request):
        Updates the operational mode settings in the configuration file using data provided in a JSON payload.
    """

    def get(self, request):
        try:
            config.clear()
            config.read(list_path_menu[0])
            limitation = 'No' if config.get(
                'functioning', 'enable_active_limitation') == "False" else 'Yes'
            compensation = 'No' if config.get(
                'functioning', 'enable_reactive_compensation') == "False" else 'Yes'
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
            config.clear()
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)

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

            if compensation == "Yes":
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
            return JsonResponse({"message": "Updated data"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error updating data, {e}"}, status=400)


class FormDataSettingDataBase(View):
    """
    View class for retrieving and updating database retention settings.

    This class handles GET and PUT requests for managing database settings. The settings
    include 'old_days', which represents the number of days to retain old data, and 
    'await_to_while', which specifies the waiting time for certain operations. These 
    settings are read from and written to a configuration file whose path is specified 
    by list_path_menu[0].

    Methods:
    --------
    get(request):
        Retrieves the current database configuration settings.

    put(request):
        Updates the database configuration settings with new values provided in the JSON payload.
    """

    def get(self, request):
        try:
            config.clear()
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
            config.clear()
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data."}, status=400)

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

            return JsonResponse({"message": "Error updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error updating data, {e}"}, status=400)


class FormDataSettingInterface(View):
    """
    View class for retrieving and updating internet interface settings.

    This view provides GET and PUT endpoints for managing configuration settings related 
    to the internet interface. The GET method retrieves the current settings, such as the 
    interface name and connection name, while the PUT method updates these settings based 
    on a JSON payload provided by the client.

    Methods:
    --------
    get(request):
        Retrieves the current internet interface settings from the configuration.

    put(request):
        Updates the internet interface settings in the configuration file using data from a JSON payload.
    """

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
            config.clear()
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data.s"}, status=400)

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
            return JsonResponse({"message": "Updated data"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error while updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataLimitation(View):
    """
    View class for retrieving and updating active energy limitation settings.

    This view handles GET and PUT requests for managing configuration settings related
    to active energy limitation. The GET method retrieves current settings from a configuration
    file (specified by list_path_menu[4]), including whether a three-phase energy meter is used,
    the meter IDs, inverter IDs, active power percentage, and grid/inverter limits. The PUT method
    validates and updates these settings based on a JSON payload from the client.

    Methods:
    --------
    get(request):
        Retrieves the current active energy limitation configuration settings.

    put(request):
        Updates the active energy limitation configuration settings after validating the input data.
    """

    def get(self, request):
        try:
            config.clear()
            config.read(list_path_menu[4])
            limitation = "Yes" if config.getboolean(
                'Active', 'energy_meter_3p', fallback=False) else "No"
            sample_data = {
                "limitation": limitation,
                "meter_ids": config.get('Active', 'energy_meter_ids', fallback="1"),
                "inverter_ids": config.get('Active', 'inverter_ids', fallback="1"),
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
            config.clear()

            config.read(list_path_menu[4])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

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
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataCompensation(View):
    """
    View class for retrieving and updating reactive power compensation settings.

    This view manages configuration settings related to reactive power compensation, 
    which are stored in a configuration file specified by list_path_menu[5]. The GET 
    method retrieves the current configuration, including whether the reactive power 
    limiter is enabled, energy meter IDs, smart logger ID, high and low reactive power 
    percentages, reactive and active offsets, active power time, and the minimum power factor.
    The PUT method updates these settings based on a JSON payload provided by the client.

    Methods:
    --------
    get(request):
        Retrieves the current reactive power compensation settings from the configuration file.

    put(request):
        Validates and updates the reactive power compensation settings using data provided 
        in the JSON payload, then writes the updated configuration back to the file.
    """

    def get(self, request):
        try:
            config.clear()
            config.read(list_path_menu[5])
            sample_data = {
                "kind": config.get("Reactive", "kind_compensation"),
                "meter_ids": config.get("Reactive", "energy_meter_ids"),
                "device": config.get("Reactive", "devices_ids",),
                "high": config.getfloat("Reactive", "reactive_power_percentage_high"),
                "low": config.getfloat("Reactive", "reactive_power_percentage_low"),
                "band_high": config.getfloat("Reactive", "reactive_band_high_limit"),
                "band_low": config.getfloat("Reactive", "reactive_band_low_limit"),
                "reactive": config.getint("Reactive", "reactive_offset"),
                "active": config.getint("Reactive", "active_offset"),
                "time": config.getfloat("Reactive", "pf_min"),
                "factor": config.getfloat("Reactive", "mu"),
            }
            return JsonResponse(sample_data)
        except Exception as ex:
            return JsonResponse({"message": str(ex)}, status=404)
    def put(self, request):
        try:
            config.clear()
            config.read(list_path_menu[5])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

            kind = data.get("selectedValue")
            meter_ids = data.get("meter_ids")
            device = data.get("device")
            high = data.get("high")
            low = data.get("low")
            band_hight=data.get("band_hight")
            band_low=data.get("band_low")
            reactive = data.get("reactive")
            active = data.get("active")
            time = data.get("time")
            factor = data.get("factor")
            
            config.set("Reactive","kind_compensation",kind)
            config.set("Reactive", "energy_meter_ids", meter_ids)
            config.set(
                "Reactive", "devices_ids", device)
            config.set("Reactive","reactive_power_percentage_high",high,)
            config.set("Reactive","reactive_power_percentage_low",low,
            
            )
            config.set("Reactive","reactive_band_high_limit",band_hight)
            config.set("Reactive","reactive_band_low_limit",band_low)
            config.set("Reactive", "reactive_offset", reactive
            )
            config.set(
                "Reactive", "active_offset", active
            )

            config.set(
                "Reactive", "pf_min", time
            )
            config.set("Reactive", "mu", factor)
            with open(list_path_menu[5], "w") as configfileChecked:
                config.write(configfileChecked)
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataBasePropierties(View):
    """
    View class for retrieving and updating database configuration properties.

    This class provides GET and PUT endpoints to manage the database connection settings.
    The GET method retrieves the current database properties such as host, port, database name,
    connection timeout, and date format (with fallback values provided if not set).
    The PUT method updates these properties in the configuration file based on a JSON payload
    from the client.

    Methods:
    --------
    get(request):
        Reads the configuration file and returns the current database properties.

    put(request):
        Validates and updates the database properties in the configuration file using data 
        provided in the JSON payload.
    """

    def get(self, request):
        try:
            config.clear()
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
            config.clear()
            config.read(list_path_menu[1])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

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
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataSettingLogs(View):
    """
    View class for retrieving and updating logging configuration settings.

    This class provides GET and PUT endpoints to manage the application's logging settings.
    The settings include the logging level, stdout output, log file path, sample logging flag,
    maximum log file size in bytes, and the backup count. These settings are read from or written
    to a configuration file specified by a global list `list_path_menu`.

    Methods:
    --------
    get(request):
        Retrieves the current logging configuration settings from the configuration file.

    put(request):
        Updates the logging configuration settings in the configuration file based on the provided
        JSON payload after validating the input data.
    """

    def get(self, request):
        try:
            config.clear()
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
            config.clear()
            config.read(list_path_menu[0])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

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
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Invalid data: one or more records contain invalid or null data, {e}"}, status=400)


class FormDataModemChecker(View):
    """
    View class for retrieving and updating modem checker configuration data.

    This view handles GET and PUT HTTP requests to manage configuration settings 
    for modem checking. The GET method retrieves current modem settings such as 
    the connection name and the attempts state. The PUT method updates these settings 
    by processing a JSON payload from the client and writing the updated values to 
    the configuration file.

    Methods:
    --------
    get(request):
        Reads the configuration file and returns the current modem settings.

    put(request):
        Validates and updates the modem settings in the configuration file based on 
        the provided JSON payload.
    """

    def get(self, request):
        try:
            config.clear()
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
            config.clear()
            config.read(list_path_menu[3])
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

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
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataSignalChecker(View):
    """
    View class for retrieving and updating signal checker configuration data.

    This class provides GET and PUT methods to handle configuration settings related 
    to signal quality. The GET method retrieves current signal quality parameters for GSM 
    and WiFi, while the PUT method allows updating these parameters.

    Methods:
    --------
    get(request):
        Reads the configuration file and returns the current signal quality parameters.

    put(request):
        Updates the configuration file with new signal quality parameters after validating 
        the input data.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve the current signal quality configuration values.

        This method reads the configuration file specified by the global list `list_path_menu` 
        and extracts the 'min_quality_gsm' and 'min_quality_wifi' values from the 
        'SIGNAL_CHECKER' section. The retrieved values are returned in a JSON response 
        under the keys 'onomondo' and 'minimum', respectively.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON object containing the current signal quality values, or an error 
                          message if an exception occurs.
        """
        try:
            config.clear()
            config.read(list_path_menu[3])
            sample_data = {
                "onomondo": config.get('SIGNAL_CHECKER', 'min_quality_gsm'),
                "minimum": config.get('SIGNAL_CHECKER', 'min_quality_wifi'),


            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    def put(self, request):
        """
        Handles PUT requests to update the signal quality configuration values.

        This method parses the JSON payload from the request to obtain new values for signal quality 
        (GSM and WiFi). It validates the input data to ensure that no value is None or an empty string. 
        If the data is valid, it updates the corresponding configuration entries in the 'SIGNAL_CHECKER' 
        section and writes the changes back to the configuration file.

        Args:
            request: The HTTP request object containing the JSON payload with new configuration values.

        Returns:
            JsonResponse: A JSON object indicating successful data update, or an error message if the input 
                          data is invalid or an exception occurs.

        Raises:
            JSONDecodeError: If the request body does not contain valid JSON.
            Exception: For any other errors encountered during processing or writing the configuration.
        """
        try:
            data = json.loads(request.body)
            config.clear()
            config.read(list_path_menu[3])
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

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
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataServerChecker(View):
    """
    View that handles server configuration data related to server checks. 
    It allows for retrieving and updating configuration data such as the number of max attempts 
    for server checks.

    Methods:
    --------
    get(request):
        Handles GET requests to retrieve the current 'max_attempts' configuration value.

    put(request):
        Handles PUT requests to update the 'max_attempts' configuration value.
        Validates the input data and writes the changes to the configuration file.
    """

    def get(self, request):
        try:
            config.clear()
            config.read(list_path_menu[3])
            sample_data = {
                "requests": config.get('SERVER_CHECKER', 'max_attempts'),


            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    def put(self, request):
        try:
            config.clear()
            config.read(list_path_menu[3])

            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

            requests = data.get("requests")
            config.set(
                'SERVER_CHECKER', 'max_attempts', requests,
            )
            with open(list_path_menu[3], "w") as configfile:
                config.write(configfile)
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)


class FormDataAwsService(APIView):
    def get(self, request):
        try:
            config.clear()
            config.read(list_path_menu[3])
            sample_data = {
                "client": config.get('AWSIOT_SERVICE', 'client_id'),
                "certificate": config.get('AWSIOT_SERVICE', 'certificate_path'),
                "private": config.get('AWSIOT_SERVICE', 'private_key_path')

            }
            return JsonResponse(sample_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    def put(self, request):
        try:
            config.clear()
            config.read(list_path_menu[3])
            data = json.loads(request.body)
            if any(value is None or value == "" for value in data.values()):
                return JsonResponse({"message": "Invalid data: one or more records contain invalid or null data"}, status=400)

            client = data.get("client")
            certicate = data.get("certicate")
            private = data.get("private")
            config.set('AWSIOT_SERVICE', 'client_id', client)
            config.set('AWSIOT_SERVICE', 'certificate_path', certicate)
            config.set('AWSIOT_SERVICE', 'private_key_path', private)

            with open(list_path_menu[3], "w") as configfile:
                config.write(configfile)
            return JsonResponse({"message": "Data updated"}, status=200)

        except json.JSONDecodeError:

            return JsonResponse({"message": "Error when updating data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Error when updating data, {e}"}, status=400)
