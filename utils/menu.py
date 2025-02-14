
import configparser
from dataclasses import dataclass, field
import os
import threading
import time
from typing import List


@dataclass
class Menu:
    list_config: List[configparser.ConfigParser] = field(init=False)

    def __post_init__(self):
        self.config = configparser.ConfigParser()

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