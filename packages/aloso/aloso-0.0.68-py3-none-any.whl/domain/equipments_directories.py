import logging
from dataclasses import dataclass

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class EquipmentsDirectories:
    name_equipment_directory: str
    directory_path: str
    server_host: str
    server_user: str
    # server_password: str
    frequency: int

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
