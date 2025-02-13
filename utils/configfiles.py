from typing import List
from dataclasses import dataclass, field


@dataclass
class configfilepaths:
    ### configuration files default locations
    main_config_path: str = field(default="/etc/enrg/utilitymanager/main_config.ini")
    db_config_path: str = field(default="/etc/enrg/utilitymanager/database_config.ini")
    modbus_config_path: str = field(default="/etc/enrg/utilitymanager/modbus_config.ini")
    http_data_config_path: str = field(default="/etc/enrg/utilitymanager/httpdatadriver_config.ini")
    active_limit_config_path: str = field(default="/etc/enrg/utilitymanager/activelimitation_config.ini")
    reactive_compensation_config_path: str = field(default="/etc/enrg/utilitymanager/compensationreactive_config.ini")

    def to_list(self) -> List[str]:
        return [
            self.main_config_path,
            self.db_config_path,
            self.modbus_config_path,
            self.http_data_config_path,
            self.active_limit_config_path,
            self.reactive_compensation_config_path,
        ]
