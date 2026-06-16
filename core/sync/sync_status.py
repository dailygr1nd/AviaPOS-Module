from enum import Enum


class SyncStatus(str, Enum):

    PENDING = "PENDING"

    PROCESSING = "PROCESSING"

    SYNCED = "SYNCED"

    FAILED = "FAILED"