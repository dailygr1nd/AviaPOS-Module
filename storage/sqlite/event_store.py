import json
import sqlite3

from core.events.base import Event
from sync.status import SyncStatus


class EventStore:

    def __init__(
        self,
        db_path: str
    ):

        self.conn = sqlite3.connect(
            db_path
        )

        self.conn.row_factory = (
            sqlite3.Row
        )

    def append(
        self,
        event: Event
    ):

        self.conn.execute(

            """
            INSERT INTO events(

                event_id,
                merchant_id,
                event_type,
                timestamp,

                previous_hash,
                payload_hash,

                payload,

                sync_status

            )

            VALUES(
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,

            (

                event.event_id,

                event.merchant_id,

                event.event_type,

                event.timestamp,

                event.previous_hash,

                event.payload_hash,

                json.dumps(
                    event.payload
                ),

                SyncStatus.PENDING.value
            )
        )

        self.conn.commit()

def latest_hash(

    self,

    merchant_id

):

    row = self.latest_event(
        merchant_id
    )

    if not row:

        return "GENESIS"

    return row[
        "event_hash"
    ]

def replay_events(

    self,

    merchant_id

):

    rows = self.all_events(
        merchant_id
    )

    return [

        dict(row)

        for row in rows

    ]