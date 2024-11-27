"""This module keeps the App level configurations"""
import os
from dataclasses import dataclass, field
from os import getenv
from typing import List
from urllib.parse import urljoin


## Flags for request/response json saving
# STORE_JSON = False
# JSON_STORAGE_PATH = "/var/data/efs/cidc/pwcar/"



@dataclass(frozen=True)
class LogConfig:
    LOG_LEVEL = "DEBUG"
    LOGGER_NAME: str = "ameristar-logger"
    LOG_FORMAT: str = "[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s] [%(funcName)s:%(lineno)s] [%(id_)s]: %(message)s"
    LOG_MAX_BYTES: str = 10**6
    LOG_BACKUP_COUNT: str = 1
    LOG_INFO_FILE_PATH: str = "ameristar_wrapper_info.log"
    LOG_ERROR_FILE_PATH: str = "ameristar_wrapper_error.log"