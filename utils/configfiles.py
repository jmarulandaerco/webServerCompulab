from typing import List
from dataclasses import dataclass, field


@dataclass
class configfilepaths:
    ### configuration files default locations
    main_config_path: str = field(default="/FW/config.ini")
    db_config_path: str = field(default="/FW/DataBase/config.ini")
    modbus_config_path: str = field(default="/FW/Modbus/config.ini")
    http_data_config_path: str = field(default="/FW/HttpDataDriver/config.ini")
    active_limit_config_path: str = field(default="/FW/ActiveLimitation/config.ini")
    reactive_compensation_config_path: str = field(default="/FW/CompensationReactive/config.ini")

    def to_list(self) -> List[str]:
        return [
            self.main_config_path,
            self.db_config_path,
            self.modbus_config_path,
            self.http_data_config_path,
            self.active_limit_config_path,
            self.reactive_compensation_config_path,
        ]
