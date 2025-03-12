from dataclasses import dataclass
import subprocess
import serial
import time

from utils.logger import LoggerHandler

logger = LoggerHandler().get_logger()

@dataclass
class WhiteList:
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

        except serial.SerialException as ex:
            logger.error(f"Error accessing the serial port: {ex}")
            return f"Error accessing the serial port: {ex}"
    
    def control_modem_service(self,start_service: bool)->bool:
        action = "start" if start_service else "stop"
        
        try:
            result = subprocess.run(
                ["sudo", "systemctl", action, "ModemManager.service"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error while trying {action} the service: {e.stderr.decode()}")
            logger.error(f"Error while trying {action} the service: {e.stderr.decode()}")
            return False



