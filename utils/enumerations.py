from enum import Enum

class ServerDBType(str, Enum):
    """
    Enum representing different types of databases.

    Database Types:
      - telemetry: Telemetry database erco
      - neu_plu: Neu_Plus database neu
    """

    TELEMETRY = "telemetry"
    NEU_PLUS = "neu_plus"

    def __str__(self) -> str:
        return self.value

class InternetInterfaceEnum(str, Enum):
    """
    Enumeration defining different internet interfaces.

    Interfaces:
        - ETHERNET: Ethernet connection
        - WIFI: Wi-Fi connection
        - GPRS: General Packet Radio Service (GPRS) connection
    """
    ETHERNET0 = "eth0"
    ETHERNET1 = "eth1"
    WIFI = "wlan0"
    GPRS = "wwan0"

    def __str__(self) -> str:
        return self.value


class ModemSignalQualityEnum(str, Enum):

    LTE = "LTE"
    GSM = "GSM"
    UMTS = "UMTS"
    UNKNOWN = "UNKNOWN"
    RSSI = "rssi"

    def __str__(self) -> str:
        return self.value
