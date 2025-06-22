from dataclasses import dataclass, field
import configparser
import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu
import asyncio
import logging

@dataclass
class SingleDeviceRead:
    """
    A class for reading Modbus registers from a single device using either RTU or TCP mode.

    This class is designed to configure and manage a Modbus client connection, retrieve data from a device,
    and log the results. The connection settings and Modbus parameters are loaded from a configuration file.

    Attributes:
    -----------
    name_config : str
        The path to the configuration file containing the Modbus settings.
    logger : logging.Logger
        A logger instance used to log messages throughout the class operations.
    mode_read : str
        The mode of communication, either 'RTU' (for Modbus RTU) or 'TCP' (for Modbus TCP).
    max_attempts : int
        The maximum number of connection attempts allowed.
    timeout_attempts : int
        The timeout for each attempt in seconds.
    serial_port : str
        The serial port to use for RTU connections (default is '/dev/ttymxc1').
    baudrate : int
        The baud rate for the Modbus RTU connection (default is 9600).
    host : str
        The host address for Modbus TCP connections (default is '127.0.0.1').
    port : int
        The port number for Modbus TCP connections (default is 502).
    slave_id : int
        The Modbus slave ID of the device to communicate with.
    modbus_function : int
        The Modbus function code to use for reading registers (e.g., 3 for holding registers).
    address_init : int
        The initial address of the first register to read.
    total_registers : int
        The total number of registers to read.

    Methods:
    --------
    __post_init():
        Reads the configuration file and initializes the class attributes.
    __start_connection():
        Starts the connection to the Modbus device using either RTU or TCP.
    __close_connection(client):
        Closes the Modbus client connection.
    run_async_simple_client():
        Starts the client connection, reads the Modbus registers asynchronously, and returns the result.
    main():
        Initializes logging, starts the Modbus client, retrieves the data, and logs the results.
    """
    name_config: str = field(init=True)
    logger: logging.Logger = field(init=False)
    mode_read: str = field(init=False)
    max_attempts: int = field(init=False)
    timeout_attempts: int = field(init=False)
    serial_port: str = field(init=False, default="/dev/ttymxc1")
    baudrate: int = field(init=False, default=9600)
    host: str = field(init=False, default="127.0.0.1")
    port: int = field(init=False, default=502)
    slave_id: int = field(init=False)
    modbus_function: int = field(init=False)
    address_init: int = field(init=False)
    total_registers: int = field(init=False)
    values: list[int] = field(init=False)

    def __post_init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.name_config)

        self.mode_read = self.config.get("Default", "mode_read")
        self.max_attempts = self.config.getint("Default", "max_attempts")
        self.timeout_attempts = self.config.getint("Default", "timeout_attempts")
        self.serial_port = self.config.get("Configuration", "serial_port")
        self.baudrate = self.config.getint("Configuration", "baudrate")
        self.host = self.config.get("Configuration", "host")
        self.port = self.config.getint("Configuration", "port")
        self.slave_id = self.config.getint("Configuration", "slave_id")
        self.modbus_function = self.config.getint("Configuration", "modbus_function")
        self.address_init = self.config.getint("Configuration", "address_init")
        self.total_registers = self.config.getint("Configuration", "total_registers")
        values_str = self.config.get("Configuration", "values", fallback="")
        self.values = [int(v.strip()) for v in values_str.split(",") if v.strip().isdigit()]

    async def __start_connection(self) -> pymodbus.client:
        try:
            if self.mode_read == "RTU":
                client = pymodbus.client.AsyncModbusSerialClient(
                    port=self.serial_port,
                    framer=pymodbus.framer.ModbusRtuFramer,
                    timeout=self.timeout_attempts,
                    retries=self.max_attempts,
                    # retry_on_empty=False,
                    # strict=True,
                    baudrate=self.baudrate,
                    bytesize=8,
                    parity="N",
                    stopbits=1,
                    # handle_local_echo=False,
                )
            elif self.mode_read == "TCP":
                client = pymodbus.client.AsyncModbusTcpClient(
                    host=self.host,
                    port=self.port,
                    framer=pymodbus.framer.ModbusSocketFramer,
                    timeout=self.timeout_attempts,
                    retries=self.max_attempts,
                )
            else:
                self.logger.warning("Invalid mode")

            self.logger.info("Connecting to slave")
            await client.connect()

            if client.connected:
                self.logger.info("Connected successfully")
                return client
            else:
                self.logger.error("Failed to connect to the Modbus server")
                return None
        except Exception as e:
            self.logger.error(f"Exception in start_connection: {e}")
            return None

    def __close_connection(self, client: pymodbus.client) -> None:
        try:
            if client is not None:
                self.logger.info("Closing connection")
                client.close()
        except Exception as e:
            self.logger.error(f"Exception in close_connection: {e}")

    async def run_async_simple_client(
        self,
    ) -> list:

        client = await self.__start_connection()

        if client is None:
            return

        self.logger.info("Getting data")
        try:
            if self.modbus_function == 3:
                rr = await client.read_holding_registers(
                    address=self.address_init,
                    count=self.total_registers,
                    slave=self.slave_id,
                )
            else:
                rr = await client.read_input_registers(
                    address=self.address_init,
                    count=self.total_registers,
                    slave=self.slave_id,
                )

            if rr.isError():
                self.logger.error(f"Exception reading registers: {rr}")
                return None
            if isinstance(rr, pymodbus.pdu.ExceptionResponse):
                self.logger.error(f"Exception in instance of Modbus library: {rr}")
                return None

            return rr.registers if rr else None
        except pymodbus.exceptions.ModbusException as e:
            self.logger.error(f"Modbus library exception: {e}")
            return None
        finally:
            self.__close_connection(client=client)

    
    async def write_registers_async(self) -> bool:
        """
        Escribe registros Modbus usando función 6 (único registro) o 16 (múltiples registros).

        Parameters:
        -----------
        values : list[int]
            Lista de valores enteros a escribir. Si se usa función 6, solo se tomará el primero.

        Returns:
        --------
        bool
            True si la escritura fue exitosa, False en caso contrario.
        """
        client = await self.__start_connection()

        if client is None:
            return False

        try:
            if self.modbus_function == 6:
                value = self.values[0] if self.values else 0
                self.logger.info(f"Writing single register at {self.address_init}: {value}")
                result = await client.write_register(
                    address=self.address_init,
                    value=value,
                    slave=self.slave_id,
                )
            elif self.modbus_function == 10:
                self.logger.info(f"Writing multiple registers at {self.address_init}: {self.values}")
                result = await client.write_registers(
                    address=self.address_init,
                    values=self.values,
                    slave=self.slave_id,
                )
            else:
                self.logger.error(f"Unsupported write function: {self.modbus_function}")
                return False

            if result.isError():
                self.logger.error(f"Error writing registers: {result}")
                return False

            self.logger.info("Registers written successfully")
            return True

        except pymodbus.exceptions.ModbusException as e:
            self.logger.error(f"Modbus write exception: {e}")
            return False

        finally:
            self.__close_connection(client)
    def mainWrite(self) -> None:
        try:
            # Crear logger
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            self.logger.propagate = False

            for handler in list(self.logger.handlers):
                self.logger.removeHandler(handler)

            formatter = logging.Formatter(
                "%(asctime)s.%(msecs)03d %(module)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            file_handler = logging.FileHandler("/var/log/enrg/modbus_read.log")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

         

            success = asyncio.run(
                self.write_registers_async(),
                debug=False
            )

            if success:
                self.logger.info("✅ Modbus write successfully completed")
            else:
                self.logger.error("❌ Modbus write failed")

        except Exception as e:
            self.logger.error(f"Exception in main (script): {e}")
    def main(self) -> None:
        try:
            # Crear un logger
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)

            # Evitar propagación a otros loggers (como el root logger que usa 'menu.log')
            self.logger.propagate = False

            # Eliminar manejadores previos de forma segura
            for handler in list(self.logger.handlers):  # Copia la lista para evitar errores
                self.logger.removeHandler(handler)

            # Crear formato de log
            formatter = logging.Formatter(
                "%(asctime)s.%(msecs)03d %(module)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # Configurar el archivo de log correcto
            file_handler = logging.FileHandler("/var/log/enrg/modbus_read.log")
            file_handler.setFormatter(formatter)

            # Agregar manejador al logger (solo archivo, sin consola)
            self.logger.addHandler(file_handler)

            read_registers = asyncio.run(
                self.run_async_simple_client(),
                debug=False,
            )

            if read_registers is not None:
                self.logger.info(f"Registers: {read_registers}")
            else:
                self.logger.error("Failed to read registers")

        except Exception as e:
            self.logger.error(f"Exception in main: {e}")
