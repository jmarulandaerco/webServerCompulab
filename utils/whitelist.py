from dataclasses import dataclass
import subprocess
import serial
import time

from utils.logger import LoggerHandler

logger = LoggerHandler().get_logger()

@dataclass
class WhiteList:
    """
    A class representing the modem's whitelist management. It allows sending AT commands 
    to a modem and controlling the modem service.

    Attributes:
    - port (str): The serial port to which the modem is connected (default: '/dev/ttyUSB3').
    - baud_rate (int): The baud rate for serial communication (default: 115200).
    """
    port:str='/dev/ttyUSB3'
    baud_rate:int=115200
    
    def send_at_command(self,command:str)->str:
        """
        Sends an AT command to the modem and displays the response.

        Args:
        port: The serial port to which the modem is connected (e.g., '/dev/ttymxc0').
        baud_rate: The baud rate for serial communication (e.g., 115200).
        command: The AT command to send (e.g., 'AT+CRSM=214,28539,0,0,12,"FFFFFFFFFFFFFFFFFFFFFFFF"').
        """
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=5)
            ser.write((command + '\r').encode())
            time.sleep(1)  
            response = ser.read_all().decode()

            print("Modem response for command:")
            print(command)
            print(response)

            ser.close()
            
            return True

        except serial.SerialException as ex:
            logger.error(f"Error accessing the serial port: {ex}")
            return False
    
    def control_modem_service(self,start_service: bool)->bool:
        action = "start" if start_service else "stop"
      
        print(action)
        try:
            result = subprocess.run(
                ["sudo", "systemctl", action, "ModemManager.service"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("Resultado de result")
            if result.returncode == 0:
                print("Comando ejecutado exitosamente")
                print(f"Resultado: {result.stdout.decode()}")  # Mostrar salida estándar si es necesario
                return True
            else:
                print(f"El servicio no se pudo controlar. Código de error: {result.returncode}")
                print(f"Salida de error: {result.stderr.decode()}")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error while trying {action} the service: {e.stderr.decode()}")
            logger.error(f"Error while trying {action} the service: {e.stderr.decode()}")
            return False



