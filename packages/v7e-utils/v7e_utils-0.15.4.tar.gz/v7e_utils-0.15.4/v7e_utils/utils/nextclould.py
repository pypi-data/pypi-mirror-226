from __future__ import annotations

import base64
import logging
from nc_py_api._exceptions import NextcloudException
from nc_py_api import Nextcloud as Next
from typing import Dict, Optional
from v7e_utils.utils.config import next_cloud_config, NextCloudItem
from dataclasses import dataclass
from datetime import datetime
from PIL import Image
from io import BytesIO


logger = logging.getLogger(__name__)


# def img_b64decode(img_encoded:str, extension:str):
#         if extension.startswith('.'): 
#             extension = extension.replace('.', '')
#         img_name = f"{int(datetime.timestamp(datetime.now()))}.{extension}"
#         decoded_img = base64.b64decode(img_encoded)
#         with Image.open(BytesIO(base64.b64decode(base64_bytes))) as img:
#             img.save(img_name, extension.upper())
#         return img

class Nextcloud:
    """
    Clase que encapsula la funcionalidad para interactuar con una instancia de Nextcloud.

    Args:
        config_parameters (NextCloudItem): Parámetros de configuración para la instancia de Nextcloud.

    Methods:
        mkdir(): Crea un directorio en la instancia de Nextcloud.\n

    """

    def __init__(self, config_parameters: NextCloudItem | None=None) -> None:

        self.username = config_parameters.username if config_parameters else next_cloud_config.username
        self.password = config_parameters.password if config_parameters else next_cloud_config.password
        self.host = config_parameters.host if config_parameters else next_cloud_config.host
        self.nc = Next(nextcloud_url=self.host,
                       nc_auth_user=self.username, nc_auth_pass=self.password)

    def mkdir(self, path: str) -> bool:
        """
        Crea un directorio y subdirectorios en la instancia de Nextcloud.

        Args:
            path (str): Ruta del directorio a crear.

        Returns:
            bool: True si el directorio se crea exitosamente, False si no.
        """
        path = path.strip()
        if path:
            try:
                # path = path of the directories to be created.
                # exist_ok= ignore error if any of pathname components already exists.
                self.nc.files.makedirs(path=path, exist_ok=True)
                return True
            except NextcloudException as e:
                logger.error(
                    f"nextcloud connection error: reason: {e.reason}, path:{path}, username:{self.username}, password:{self.password}, host:{self.host}")
        return False
