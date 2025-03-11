import serial
import time

def send_at_command(port, baud_rate, command):
    """
    Sends an AT command to the modem and displays the response.

    Args:
    port: The serial port to which the modem is connected (e.g., '/dev/ttymxc0').
    baud_rate: The baud rate for serial communication (e.g., 115200).
    command: The AT command to send (e.g., 'AT+CRSM=214,28539,0,0,12,"FFFFFFFFFFFFFFFFFFFFFFFF"').
    """
    try:
        ser = serial.Serial(port, baud_rate, timeout=5)
        ser.write((command + '\r').encode())
        time.sleep(1)  # Wait to receive the response
        response = ser.read_all().decode()

        print("Modem response for command:")
        print(command)
        print(response)

        ser.close()

    except serial.SerialException as e:
        print(f"Error accessing the serial port: {e}")


if __name__ == "__main__":
    serial_port = '/dev/ttyUSB2'  # Adjust as needed
    baud_rate = 115200             # Adjust as needed

    # AT commands to execute

    at_command_delete = 'AT+COPS=1,2,"732123"'
    #at_command_restore = 'AT+COPS=0'
    at_command_clear = 'AT+CRSM=214,28539,0,0,12,"FFFFFFFFFFFFFFFFFFFFFFFF"'

    send_at_command(serial_port, baud_rate, at_command_delete)
    send_at_command(serial_port, baud_rate, at_command_clear)
    time.sleep(1)
