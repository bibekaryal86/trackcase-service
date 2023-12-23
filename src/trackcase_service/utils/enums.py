from enum import Enum


class LogLevelOptions(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


class Statuses(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CLOSED = "CLOSED"
    RETIRED = "RETIRED"
    DISABLED = "DISABLED"
