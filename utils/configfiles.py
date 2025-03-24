from typing import List
from dataclasses import dataclass, field


@dataclass
class ConfigFilePaths:
    """
    Stores the file paths of various configuration files used in the system.

    Attributes:
        main_config_path (str): Path to the main configuration file.
        db_config_path (str): Path to the database configuration file.
        modbus_config_path (str): Path to the Modbus configuration file.
        http_data_config_path (str): Path to the HTTP data driver configuration file.
        active_limit_config_path (str): Path to the active limitation configuration file.
        reactive_compensation_config_path (str): Path to the reactive compensation configuration file.
    """
    main_config_path: str = field(default="/FW/config.ini")
    db_config_path: str = field(default="/FW/DataBase/config.ini")
    modbus_config_path: str = field(default="/FW/Modbus/config.ini")
    http_data_config_path: str = field(default="/FW/HttpDataDriver/config.ini")
    active_limit_config_path: str = field(default="/FW/ActiveLimitation/config.ini")
    reactive_compensation_config_path: str = field(default="/FW/CompensationReactive/config.ini")

    # main_config_path: str = field(default="/etc/enrg/utilitymanager/main_config.ini")
    # db_config_path: str = field(default="/etc/enrg/utilitymanager/database_config.ini")
    # modbus_config_path: str = field(default="/etc/enrg/utilitymanager/modbus_config.ini")
    # http_data_config_path: str = field(default="/etc/enrg/utilitymanager/httpdatadriver_config.ini")
    # active_limit_config_path: str = field(default="/etc/enrg/utilitymanager/activelimitation_config.ini")
    # reactive_compensation_config_path: str = field(default="/etc/enrg/utilitymanager/compensationreactive_config.ini")

    def to_list(self) -> List[str]:
        """
        Returns a list containing all the configuration file paths.

        Returns:
            List[str]: A list of all configuration file paths.
        """
        return [
            self.main_config_path,
            self.db_config_path,
            self.modbus_config_path,
            self.http_data_config_path,
            self.active_limit_config_path,
            self.reactive_compensation_config_path,
        ]
