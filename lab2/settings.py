import os
import sys
import psycopg2
from enum import IntEnum
from typing import Callable
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class ConsoleCommands(IntEnum):
    STANDBY = sys.maxsize
    PREV_PAGE = sys.maxsize - 1
    NEXT_PAGE = sys.maxsize - 2
    GO_BACK = sys.maxsize - 3
    CONFIRM = sys.maxsize - 4


class MessageType(IntEnum):
    INFO = 0
    SUCCESSFUL = 1
    ERROR = 2


def is_valid_str(string):
    return isinstance(string, str) and string.strip()


def exception_handler(e: Exception, rollback_cb: Callable):
    if isinstance(e, psycopg2.Error):
        rollback_cb()


DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "poshta"
DB_USER = "postgres"
DB_PASSWORD = "236450923"
