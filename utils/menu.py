
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
from pymongo import MongoClient
from django.core.management import call_command
import netifaces

@dataclass
class Menu:
    """
    Clase Menu

    Proporciona una interfaz para la administración del sistema, incluyendo servicios del sistema,
    usuarios, configuración de red, información del módem, manipulación de archivos de registro,
    y gestión de carpetas para dispositivos.

    Atributos:
        modem (SimModem): Instancia del módem utilizada para obtener información del dispositivo.
        logger (logging.Logger): Instancia del logger personalizada para registrar eventos y errores.

    Métodos:
        check_service_status() -> bool:
            Verifica si el servicio 'enrg-utilitymanager.service' está activo.

        execute_command(command: str):
            Ejecuta un comando en un hilo separado con control de errores.

        start_service() -> bool:
            Inicia o reinicia el servicio 'enrg-utilitymanager.service'.

        change_user_password(new_password: str) -> bool:
            Cambia la contraseña del usuario 'erco_config'.

        delete_log() -> bool:
            Elimina el archivo de log principal del sistema.

        stop_service() -> bool:
            Detiene el servicio 'enrg-utilitymanager.service'.

        reboot() -> bool:
            Reinicia el sistema operativo.

        view_modem_info() -> str:
            Recupera y muestra información del módem, la SIM y la calidad de la señal.

        toggle_wifi() -> str:
            Activa o desactiva la antena Wi-Fi.

        add_wifi(ssid: str, password: str, connection_name: str) -> str:
            Se conecta a una red Wi-Fi especificada.

        create_user_if_not_exists(username: str, password: str):
            Crea un usuario si no existe ya en la base de datos.

        ensure_user_collection():
            Verifica la existencia de la colección de usuarios en MongoDB y ejecuta migraciones si no existe.

        setup_folder_path() -> List[List[str]]:
            Devuelve las carpetas de dispositivos disponibles como opciones.

        clear_log_single_device():
            Limpia el contenido del log de lectura del dispositivo Modbus.

        get_ip_interface(interface: str) -> str:
            Obtiene la dirección IP asociada a una interfaz de red.

        get_gateway_interface(interface: str) -> str:
            Obtiene la puerta de enlace asociada a una interfaz de red.
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
         

            if user is not None:
                self.logger.info(f"⚠️ The user '{username}' already exists. Skipping creation.")
                return

            User.objects.create_user(username=username, password=password)
            self.logger.info(f"✅ User '{username}' created successfully.")

        except Exception as e:
            self.logger.error(f"❌ Error creating user '{username}': {e}")
    
    def update_user_password(self, username, new_password):
        try:
            user = User.objects.filter(username=username).first()
            
            if user is None:
                self.logger.warning(f"⚠️ User '{username}' does not exist. Cannot update password.")
                return

            user.set_password(new_password)
            user.save()
            self.logger.info(f"🔐 Password for user '{username}' updated successfully.")
        
        except Exception as e:
            self.logger.error(f"❌ Error updating password for user '{username}': {e}")
                
 
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
        
    

    def get_wlan_ip(self,ifname='mlan0') -> str :
        if ifname in netifaces.interfaces():
            addrs = netifaces.ifaddresses(ifname)
            ipv4 = addrs.get(netifaces.AF_INET)
            if ipv4:
                return ipv4[0].get('addr')
        return None
    

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
        
    

    def get_wlan_ip(self,ifname='Wlan0') -> str :
        if ifname in netifaces.interfaces():
            addrs = netifaces.ifaddresses(ifname)
            ipv4 = addrs.get(netifaces.AF_INET)
            if ipv4:
                return ipv4[0].get('addr')
        return None
    

    def configure_iptables(self,eth_interface: str, destination_ip: str,port:str) -> bool:
        try:
            commands = [
                f"sudo iptables -A FORWARD -i {eth_interface} -o wwan0 -j ACCEPT",
                f"sudo iptables -A FORWARD -i wwan0 -o {eth_interface} -j ACCEPT",
                f"sudo iptables -t nat -A PREROUTING -p TCP --dport 1422 -j DNAT --to-destination {destination_ip}:{port}",
                "sudo iptables -t nat -A POSTROUTING -o wwan0 -j MASQUERADE",
                f"sudo iptables -t nat -A POSTROUTING -o {eth_interface} -j MASQUERADE"
            ]

            for command in commands:
                result = subprocess.run(command, shell=True, capture_output=True)
                if result.returncode != 0:
                    return False  

            return True 

        except Exception:
            return False

    def not_configure_iptables(self,eth_interface: str, destination_ip: str,port:str) -> bool:
        try:
            commands = [
                f"sudo iptables -D FORWARD -i {eth_interface} -o wwan0 -j ACCEPT",
                f"sudo iptables -D FORWARD -i wwan0 -o {eth_interface} -j ACCEPT",
                f"sudo iptables -t nat -D PREROUTING -p TCP --dport 1422 -j DNAT --to-destination {destination_ip}:{port}",
                "sudo iptables -t nat -D POSTROUTING -o wwan0 -j MASQUERADE",
                f"sudo iptables -t nat -D POSTROUTING -o {eth_interface} -j MASQUERADE"
            ]

            for command in commands:
                result = subprocess.run(command, shell=True, capture_output=True)
                if result.returncode != 0:
                    return False  

            return True 

        except Exception:
            return False
        
    def clear_word(self,texto: str) -> str:
        # Elimina cualquier palabra que contenga "Modbus" o "TCP", sin importar mayúsculas/minúsculas
        return re.sub(r'\b\w*(modbus|tcp|rtu)\w*\b', '', texto, flags=re.IGNORECASE).strip()