from enum import Enum


class LogLevelOptions(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


class Status(str, Enum):
    OPEN = "OPEN"  # started
    PROCESSING = "PROCESSING"  # working on it
    PENDING = "PENDING"  # waiting on customer
    SUBMITTED = "SUBMITTED"  # submitted to uscis/court
    RFE_RECEIVED = "RFE_RECEIVED"  # received RFE from uscis/court
    APPROVED = "APPROVED"  # approved
    DENIED = "DENIED"  # denied
    CLOSED = "CLOSED"  # closed
    RECEIVED = "RECEIVED"  # eg: payment received, form received
    WAIVED = "WAIVED"  # eg: payment waived
