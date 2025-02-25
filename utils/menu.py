
import configparser
from dataclasses import dataclass, field
import os
import subprocess
import threading
import time
from typing import List
from authApp.models.user import User  # Importar modelos después de django.setup()
from pymongo import MongoClient
from django.contrib.auth import get_user_model
from django.conf import settings
from utils.modem_gsm_driver import SimModem


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

    def __post_init__(self):
        self.modem = SimModem(connection_name="Red-Onomondo")

    def check_service_status(self)-> bool:
        """Check the status of a systemd service."""
        try:
            result = os.system("systemctl is-active --quiet FW_main.service")
            exit_code = os.WEXITSTATUS(result)

            if result == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def execute_command(self, command: str) :
   
        def run_command():
            os.system(command)

        command_thread = threading.Thread(target=run_command)
        command_thread.start()

        for i in range(31):

            if not command_thread.is_alive():
                break

            
            time.sleep(1)

        command_thread.join()

    def start_service(self)-> bool:
        """Start a systemd service, or restart if it's already active, with a progress bar."""

        status = self.check_service_status()
        try:
            if status == True:
                command = "sudo systemctl restart FW_main.service"
                self.execute_command(command)
            elif status == False:
                command = "sudo systemctl start FW_main.service"
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
        except Exception :
            return False
        
    def change_user_password(self, new_password):
        try:
            os.system(f"echo 'erco_config:{new_password}' | sudo chpasswd")
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
        
    def delete_log(self):
        try:
            os.system("rm /FW/log.log")
            return True
        except Exception as e:
            print(f"Error delete log: {e}")
            return False
            

    def stop_service(self):
        """Stop and disable a systemd service."""
        status = self.check_service_status()
        if status == "inactive":
            print("Service enrg-utilitymanager.service is already stopped.")
            return False

        try:
            os.system("sudo systemctl stop FW_main.service")
            return True

        except Exception as e:
            return False
        
    def reboot(self):
        try:
            os.system("sudo reboot")
        except Exception as e:
            print("Error al reiniciar el equipo")

    
    def view_modem_info(self):
        """Displays modem, SIM, and signal information in a dialog menu."""
        try:
            if not self.modem.is_modem_present():
                return "Modem not present."

            ip_sim = subprocess.check_output(
                "ip a show wwan0 | awk '/inet / {print $2}' | cut -d'/' -f1",
                shell=True,
                text=True,
            ).strip()
            sim_info = None
            if self.modem.is_sim_present():
                sim_info = self.modem.get_sim_info()
                if not sim_info:
                    return "SIM is present but unable to retrieve SIM info."
            else:
                
                return "SIM not present."

            if not self.modem.is_modem_connected():
                
                return "Modem is present but not connected to a network."

            signal_quality = self.modem.get_signal_quality()
            if not signal_quality:
                
                return "Unable to retrieve signal quality information."

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

            return  f"{sim_info_text}\n{signal_info_text}"
            
        except Exception as e:
            return f"Error en la obtención de datos del modem {e}"
    
    def toggle_wifi(self):

        result = subprocess.run(
            "nmcli radio wifi", shell=True, capture_output=True, text=True
        )
        current_status = result.stdout.strip()
        new_status = "off" if current_status == "enabled" else "on"
        toggle_command = f"sudo nmcli radio wifi {new_status}"
        result = subprocess.run(toggle_command, shell=True)

        if result.returncode == 0:
            return f"Wi-Fi antenna is now {new_status}."
        else:
            return "Failed to change Wi-Fi antenna state."
       

    def add_wifi(self,ssid,password,connection_name):
        try:
            result = os.system(
                            f"sudo nmcli dev wifi con '{ssid}' password '{password}' name '{connection_name}'"
                        )        
            if result != 0:
                            
                return "Failed to connect to Wi-Fi. Please check your credentials."
                            
            else:
                            
                return f"Connected to Wi-Fi network '{ssid}' with connection name '{connection_name}'."
                              
        except:
            return "Error adding wifi network"
    
    
    def create_user_if_not_exists(self, username, password):
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            print(f"✅ User '{username}' creater correct.")
        else:
            print(f"⚠️ The user '{username}' already exist.")
            
    def setup_folder_path(self):
        try:
            folders_devices=[]
            choices=[]
            path_modbus = "/FW/Modbus/modbusmaps"
            print(path_modbus)
            if os.path.exists(path_modbus):
                folders_devices = [name for name in os.listdir(path_modbus) if os.path.isdir(os.path.join(path_modbus, name))]
                
            if folders_devices:
                choices=[(str(i + 1), folder)
                        for i, folder in enumerate(folders_devices)],
                
            return[folders_devices,choices]
        except Exception as ex:
            print(ex)
            return[]
        

       