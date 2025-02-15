import re
import subprocess
import netifaces
from typing import Union, Dict
from dataclasses import dataclass, field
from .enumerations import InternetInterfaceEnum, ModemSignalQualityEnum

@dataclass
class ModemSignalQuality:
    # Attributes
    network_technology: str = field(init=False, default="None")
    RSSI: float = field(init=False, default=0.0)

@dataclass
class SimModem:
    # Public Attributes
    connection_name: str = field(init=True)
    # Private Attributes
    __modem_id: Union[None, str] = field(init=False, default=None)

    # Private Methods
    def __post_init__(self) -> None:
        self.__modem_id = self.__get_modem_id()

    def __run_bash_command(self, command:str) -> Union[None,str]:
        val_return = None
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            val_return = result.stdout.strip()
        except Exception as e:
            return None
        return val_return

    def __get_modem_id(self) -> Union[None, str]:
        val_return = None
        try:
            modem = self.__run_bash_command("mmcli -L")
            if modem:
                val_return = modem.split()[0]
        except Exception as e:
            return None

        return val_return

    # Public Methods
    def is_modem_present(self) -> bool:
        return self.__modem_id is not None

    def is_sim_present(self) -> bool:
        val_return: bool = False
        try:
            if not self.__modem_id:
                return val_return

            sim_status = self.__run_bash_command(
                f"mmcli -m {self.__modem_id} | grep 'SIM' | grep 'dbus path' | awk '{{print $5}}'"
            )
            val_return = "SIM" in sim_status
        except Exception as e:
            return False

        return val_return

    def get_sim_info(self) -> Union[None, tuple[str, str, str]]:

        try:
            if not self.__modem_id:
                return None

            # Get the SIM path
            sim_path = self.__run_bash_command(
                f"mmcli -m {self.__modem_id} | grep 'SIM' | grep 'dbus path' | awk '{{print $5}}'"
            )

            if not sim_path:
                return None

            # Get SIM information using the SIM path
            operator_sim_info = self.__run_bash_command(f"mmcli -m {self.__modem_id}")
            iccid_sim_info = self.__run_bash_command(f"mmcli -i {sim_path}")

            # Extract ICCID, Operator ID, and Operator Name using regex
            iccid_match = re.search(r"iccid:\s*(\S+)", iccid_sim_info)
            operator_id_match = re.search(r"operator id:\s*(\S+)", operator_sim_info)
            operator_name_match = re.search(
                r"operator name:\s*(\S+)", operator_sim_info
            )

            iccid = iccid_match.group(1) if iccid_match else None
            operator_id = operator_id_match.group(1) if operator_id_match else None
            operator_name = (
                operator_name_match.group(1) if operator_name_match else None
            )

        except Exception as e:
            return None
        return iccid, operator_id, operator_name

    def is_modem_connected(self) -> bool:
        try:
            val_return: bool = False

            if not self.__modem_id:
                return val_return

            modem_info = self.__run_bash_command(f"mmcli -m {self.__modem_id}")
            if "connected" in modem_info:
                val_return = True
        except Exception as e:

            return False

        return val_return

    def parse_modem_info(self, info_modem: str) -> Dict[str, Dict[str, str]]:
        try:
            val_return: dict = {}
            sections = re.split(r"\n(?=\w+)", info_modem)

            for section in sections:

                if ModemSignalQualityEnum.LTE in section:
                    network_type = ModemSignalQualityEnum.LTE
                elif ModemSignalQualityEnum.GSM in section:
                    network_type = ModemSignalQualityEnum.GSM
                elif ModemSignalQualityEnum.UMTS in section:
                    network_type = ModemSignalQualityEnum.UMTS
                else:
                    network_type = ModemSignalQualityEnum.UNKNOWN

                rssi = re.search(r"rssi:\s*(-?\d+\.?\d*)\s*dBm", section)

                if network_type not in val_return:
                    val_return[network_type] = {}

                if rssi:
                    val_return[network_type][ModemSignalQualityEnum.RSSI] = rssi.group(
                        1
                    )

        except Exception as e:
            return

        return val_return

    def get_signal_quality(self) -> Union[None, ModemSignalQuality]:
        try:
            val_return = None

            if (
                not self.is_modem_present()
                or not self.is_sim_present()
                or not self.is_modem_connected()
            ):
                return val_return

            self.__run_bash_command(
                f"sudo mmcli -m  {self.__modem_id} --signal-setup=10"
            )
            command_response = self.__run_bash_command(
                f"mmcli -m {self.__modem_id} --signal-get"
            )

            signal_quality_data = self.parse_modem_info(command_response)

            if signal_quality_data:
                val_return = ModemSignalQuality
                val_return.network_technology = next(iter(signal_quality_data))
                val_return.RSSI = float(
                    signal_quality_data[val_return.network_technology].get(
                        ModemSignalQualityEnum.RSSI, 0.0
                    )
                )

        except Exception as e:
            return None
        return val_return

    def disable_modem(self):
        if self.__modem_id:
            self.__run_bash_command(f"sudo nmcli con down {self.connection_name}")

    def set_as_default_interface(self) -> None:
        try:
            # Get information for the specified interface
            info = netifaces.ifaddresses(InternetInterfaceEnum.GPRS.value)
            ip_address = info[netifaces.AF_INET][0]["addr"]

            # Configure the default route
            self.__run_bash_command("sudo ip route del default")
            self.__run_bash_command(
                f"sudo ip route add default via {ip_address} dev {InternetInterfaceEnum.GPRS.value} proto dhcp src {ip_address} metric 201"
            )
        

        except Exception as e:
            print(e)


    def enable_modem(self):

        if self.__modem_id:
            self.__run_bash_command(f"sudo nmcli con up {self.connection_name}")

    def reset_modem(self):

        self.disable_modem()
        self.enable_modem()
