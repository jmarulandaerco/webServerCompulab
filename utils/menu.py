
from dataclasses import dataclass, field
import logging
import os
import subprocess
import threading
# Importar modelos después de django.setup()
from authApp.models.user import User
from django.contrib.auth import get_user_model
from django.conf import settings
from utils.logger import LoggerHandler
from utils.modem_gsm_driver import SimModem
import re


@dataclass
class Menu:
    """
    Provides functionalities to manage system services, user authentication, 
    modem information, Wi-Fi configuration, and file management.

    Attributes:
        modem (SimModem): An instance of SimModem used to manage modem operations.

    Methods:
        check_service_status() -> bool:
            Checks if the 'FW_main.service' systemd service is active.

        execute_command(command: str):
            Executes a command in a separate thread with a timeout of 30 seconds.

        start_service() -> bool:
            Starts or restarts the 'FW_main.service' systemd service.

        change_user_password(new_password: str) -> bool:
            Changes the password of the user 'erco_config'.

        delete_log() -> bool:
            Deletes the system log file located at '/FW/log.log'.

        stop_service() -> bool:
            Stops the 'FW_main.service' systemd service.

        reboot():
            Reboots the system.

        view_modem_info() -> str:
            Retrieves and returns modem, SIM, and network signal information.

        toggle_wifi() -> str:
            Toggles the Wi-Fi antenna state between on and off.

        add_wifi(ssid: str, password: str, connection_name: str) -> str:
            Connects to a Wi-Fi network with the given SSID and password.

        create_user_if_not_exists(username: str, password: str):
            Creates a new user if it does not already exist in the database.

        setup_folder_path() -> List[List[str]]:
            Retrieves available Modbus device folders and returns them as choices.
    """
    modem: SimModem = field(init=False)
    logger: logging.Logger = field(init=False)

    def __post_init__(self):
        self.modem = SimModem(connection_name="Red-Onomondo")
        logger_handler = LoggerHandler()
        self.logger = logger_handler.get_logger()

    def check_service_status(self) -> bool:
        """Check the status of a systemd service."""
        try:
            result = os.system(
                "sudo systemctl is-active --quiet enrg-utilitymanager.service")
            exit_code = os.WEXITSTATUS(result)
            if result == 0:
                return True
            else:
                return False

        except Exception as ex:
            self.logger.error(
                f"Error checking the status of a systemd service: {ex}")

            return False

    def execute_command(self, command: str):
        def run_command():
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error excecute console command {e}")

        command_thread = threading.Thread(target=run_command)
        command_thread.start()
        command_thread.join()

    def start_service(self) -> bool:
        """Start a systemd service, or restart if it's already active, with a progress bar."""

        status = self.check_service_status()

        try:
            if status == True:
                command = "sudo systemctl restart enrg-utilitymanager.service"
                self.execute_command(command)
            elif status == False:
                command = "sudo systemctl start enrg-utilitymanager.service"
                self.execute_command(command)
            else:
                return False
            new_status = self.check_service_status()
            if new_status == True:

                return True
            elif new_status == False:
                return False
            else:
                return False
        except Exception as ex:
            self.logger.error(f"Error started service {ex}")
            return False

    def change_user_password(self, new_password:str)->bool:
        try:
            os.system(f"echo 'erco_config:{new_password}' | sudo chpasswd")
            return True
        except Exception as e:
            self.logger.error(f"Error changing password: {e}")
            return False

    def delete_log(self) -> bool:
        try:
            os.system("rm /var/log/enrg/main.log")
            return True
        except Exception as e:
            self.logger.error(f"Error delete log: {e}")
            return False

    def stop_service(self) -> bool:
        """Stop and disable a systemd service."""
        status = self.check_service_status()
        if status == "inactive":
            return False

        try:
            os.system("sudo systemctl stop enrg-utilitymanager.service")
            return True

        except Exception as e:
            self.logger.error(f"Error stopping the service: {e}")
            return False

    def reboot(self) -> bool:
        try:
            os.system("sudo reboot")
            return True
        except Exception as e:
            self.logger.error(f"Error rebooting the computer {e}")

            return False

    def view_modem_info(self):
        """Displays modem, SIM, and signal information in a dialog menu."""
        try:
            if not self.modem.is_modem_present():
                self.logger.warning(f"Modem not present. {e}")

                return "Modem no presente"

            ip_sim = subprocess.check_output(
                "ip a show wwan0 | awk '/inet / {print $2}' | cut -d'/' -f1",
                shell=True,
                text=True,
            ).strip()
            sim_info = None
            if self.modem.is_sim_present():
                sim_info = self.modem.get_sim_info()
                if not sim_info:
                    return "La SIM está presente pero no puede recuperar la información de la SIM"
            else:

                return "SIM no presente"

            if not self.modem.is_modem_connected():

                return "Modem esta presente pero no conectado a la red"

            signal_quality = self.modem.get_signal_quality()
            if not signal_quality:

                return "Incapaz de recuperar información sobre la calidad de la señal"

            iccid, operator_id, operator_name = sim_info
            sim_info_text = (
                f"SIM Information:\n"
                f"ICCID: {iccid}\n"
                f"Operator ID: {operator_id}\n"
                f"Operator Name: {operator_name}\n"
                f"IP Sim: {ip_sim}\n"
            )

            signal_info_text = (
                f"Signal Quality:\n"
                f"Network Technology: {signal_quality.network_technology}\n"
                f"RSSI: {signal_quality.RSSI} dBm\n"
            )

            return f"{sim_info_text}\n{signal_info_text}"

        except Exception as e:
            self.logger.error(f"Error in obtaining data from the modem {e}")
            return f"Error en la obtención de datos del modem {e}"

    def toggle_wifi(self)->str:
        try:
            result = subprocess.run(
                "nmcli radio wifi", shell=True, capture_output=True, text=True
            )
            current_status = result.stdout.strip()
            new_status = "off" if current_status == "enabled" else "on"
            toggle_command = f"sudo nmcli radio wifi {new_status}"
            result = subprocess.run(toggle_command, shell=True)

            if result.returncode == 0:
                return f"la antena wi-Fi  esta {new_status}."
            else:
                return "Fallo al cambiar el estado de la antena wi-fi"
        except Exception as ex:
            self.logger.error(f"enable-disable wifi: {ex}")

    def add_wifi(self, ssid:str, password:str, connection_name:str)->str:
        try:
            result = os.system(
                f"sudo nmcli dev wifi con '{ssid}' password '{password}' name '{connection_name}'"
            )
            if result != 0:

                return "Fallo al conectar a la red Wi-Fi. Por favor revisa las credenciales"

            else:

                return f"Connectado a la red Wi-Fi  '{ssid}' con nombre '{connection_name}'."

        except Exception as ex:
            self.logger.error(f"Error adding wifi network: {ex}")
            return "Error añadiendo la red wi-fi"

    def create_user_if_not_exists(self, username, password):
        try:
            user = User.objects.filter(username=username).first()
            print("HOLA")
            print(user)
            if user == "erco_to" or user =="erco_config":
                self.logger.info(f"⚠️ The user '{username}' already exists. Skipping creation.")
                return  # No hace nada si ya existe

            User.objects.create_user(username=username, password=password)
            self.logger.info(f"✅ User '{username}' created successfully.")

        except Exception as e:
            self.logger.error(f"❌ Error creating user '{username}': {e}")

    def setup_folder_path(self):
        try:
            folders_devices = []
            choices = []
            path_modbus = "/usr/share/enrg/utilitymanager/modbusmaps"
            if os.path.exists(path_modbus):
                folders_devices = [name for name in os.listdir(
                    path_modbus) if os.path.isdir(os.path.join(path_modbus, name))]

            if folders_devices:
                choices = [(str(i + 1), folder)
                           for i, folder in enumerate(folders_devices)],

            return [folders_devices, choices]
        except Exception as ex:
            self.logger.error(f"no folder path: {ex}")
            return []

    def clear_log_single_device(self):
      # Asegurarse de que el directorio exista
        log_dir = "/var/log/enrg"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Configurar el archivo de log correcto
        log_file = os.path.join(log_dir, "modbus_read.log")

        # Borrar el contenido del archivo si ya existe o crear uno nuevo si no existe
        if os.path.exists(log_file):
            with open(log_file, 'w'):  # Abrir en modo 'w' borra el archivo
                pass
        else:
            # Crear el archivo vacío si no existe
            open(log_file, 'w').close()

    def get_ip_interface(self,interface):
        try:
            resultado = subprocess.check_output(
                ['ip', 'addr', 'show', interface], text=True)
            # Buscar línea con 'inet' que contiene la IP
            match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', resultado)
            if match:
                return match.group(1)
            else:
                return ""
        except subprocess.CalledProcessError:
            return ""
    
    def get_gateway_interface(self,interface):
        try:
            resultado = subprocess.check_output(
                ['ip', 'route', 'show', 'dev', interface],
                text=True
            )
            # Buscar línea que contiene "default via"
            match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', resultado)
            if match:
                return match.group(1)
            else:
                return f""
        except subprocess.CalledProcessError:
            return f""