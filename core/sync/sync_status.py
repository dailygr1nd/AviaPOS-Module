from enum import Enum


class SyncStatus(str, Enum):

    RECEIVED = "RECEIVED"

    PENDING = "PENDING"

    PROCESSING = "PROCESSING"

    PROCESSED = "PROCESSED"

    SYNCED = "SYNCED"

    FAILED = "FAILED"

    REJECTED = "REJECTED"


class SyncDirection(str, Enum):

    CLIENT_TO_SERVER = "CLIENT_TO_SERVER"

    SERVER_TO_CLIENT = "SERVER_TO_CLIENT"