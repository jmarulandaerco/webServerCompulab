
import configparser
from dataclasses import dataclass, field
import os
import subprocess
import threading
import time
from typing import List

from utils.modem_gsm_driver import SimModem


@dataclass
class Menu:
    list_config: List[configparser.ConfigParser] = field(init=False)
    modem: SimModem = field(init=False)

    def __post_init__(self):
        self.config = configparser.ConfigParser()
        self.modem = SimModem(connection_name="Red-Onomondo")

    def check_service_status(self)-> bool:
        """Check the status of a systemd service."""
        try:
            result = os.system("systemctl is-active --quiet enrg-utilitymanager.service")
            if result == 0:
                return True
            else:
                return False
        except Exception as e:
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
                command = "sudo systemctl restart enrg-utilitymanager.service"
                self.execute_command(command)
            elif status == False:
                command = "sudo systemctl start enrg-utilitymanager.service"
                self.execute_command(command)
            else:
                return False

            # Check the service status after the command has finished
            new_status = self.check_service_status()
            if new_status == True:
                print(
                    "Service enrg-utilitymanager.service started successfully."
                )
                return True
            elif new_status == False:
                print(
                    "Service enrg-utilitymanager.service failed to start."
                )
            else:
               
                print(
                    "Service enrg-utilitymanager.service did not start correctly."
                )
                return False

        except Exception as e:
           
            print(f"An error occurred while starting/restarting the service: {e}")
            return False
        
    def change_user_password(self, new_password):
        # Cambiar la contraseña del usuario 'erco_config'
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
            os.system("sudo systemctl stop enrg-utilitymanager.service")
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
            # Verificar si el módem está presente
            if not self.modem.is_modem_present():
                return "Modem not present."

            ip_sim = subprocess.check_output(
                "ip a show wwan0 | awk '/inet / {print $2}' | cut -d'/' -f1",
                shell=True,
                text=True,
            ).strip()
            # Verificar si la SIM está presente
            sim_info = None
            if self.modem.is_sim_present():
                sim_info = self.modem.get_sim_info()
                if not sim_info:
                    return "SIM is present but unable to retrieve SIM info."
            else:
                
                return "SIM not present."

            # Verificar si el módem está conectado
            if not self.modem.is_modem_connected():
                
                return "Modem is present but not connected to a network."

            # Obtener calidad de la señal
            signal_quality = self.modem.get_signal_quality()
            if not signal_quality:
                
                return "Unable to retrieve signal quality information."

            # Mostrar la información del SIM y señal en un cuadro de diálogo
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

            # Mostrar un cuadro de diálogo con toda la información
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
       
