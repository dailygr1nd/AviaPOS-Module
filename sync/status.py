from enum import Enum


class SyncStatus(str, Enum):

    PENDING = "PENDING"

    SYNCED = "SYNCED"

    FAILED = "FAILED"