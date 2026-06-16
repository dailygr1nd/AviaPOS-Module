import json
import sqlite3

from typing import List


class EventStore:

    def __init__(

        self,

        db_path: str

    ):

        self.db_path = db_path

    def append(

        self,

        event

    ):

        conn = sqlite3.connect(
            self.db_path
        )

        conn.execute(

            """
            INSERT INTO events (

                event_id,

                merchant_id,

                event_type,

                timestamp,

                previous_hash,

                payload_hash,

                event_hash,

                payload,

                sync_status

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (

                event.event_id,

                event.merchant_id,

                event.event_type,

                event.timestamp,

                event.previous_hash,

                event.payload_hash,

                event.event_hash,

                json.dumps(
                    event.payload
                ),

                "PENDING"

            )

        )

        conn.commit()

        conn.close()

    def replay_events(

        self,

        merchant_id: str

    ) -> List[dict]:

        conn = sqlite3.connect(
            self.db_path
        )

        conn.row_factory = (
            sqlite3.Row
        )

        rows = conn.execute(

            """
            SELECT *
            FROM events
            WHERE merchant_id = ?
            ORDER BY timestamp ASC
            """,

            (merchant_id,)

        ).fetchall()

        conn.close()

        events = []

        for row in rows:

            event = dict(row)

            event["payload"] = json.loads(

                event["payload"]

            )

            events.append(
                event
            )

        return events
    
    def latest_hash(

        self,

        merchant_id: str

    ) -> str:

        conn = sqlite3.connect(
            self.db_path
        )

        row = conn.execute(

            """
            SELECT event_hash

            FROM events

            WHERE merchant_id = ?

            ORDER BY timestamp DESC

            LIMIT 1
            """,

            (merchant_id,)

        ).fetchone()

        conn.close()

        if not row:

            return "GENESIS"

        return row[0]
    
    def count_events(

        self,

        merchant_id: str

    ) -> int:

        conn = sqlite3.connect(
            self.db_path
        )

        row = conn.execute(

            """
            SELECT COUNT(*)

            FROM events

            WHERE merchant_id = ?
            """,

            (merchant_id,)

        ).fetchone()

        conn.close()

        return row[0]
    
    def pending_events(

        self,

        merchant_id: str

    ):

        conn = sqlite3.connect(
            self.db_path
        )

        conn.row_factory = (
            sqlite3.Row
        )

        rows = conn.execute(

            """
            SELECT *

            FROM events

            WHERE merchant_id = ?

            AND sync_status = 'PENDING'

            ORDER BY timestamp ASC
            """,

            (merchant_id,)

        ).fetchall()

        conn.close()

        return [

            dict(row)

            for row in rows

        ]
    
    def mark_synced(

        self,

        event_id: str

    ):

        conn = sqlite3.connect(
            self.db_path
        )

        conn.execute(

            """
            UPDATE events

            SET sync_status='SYNCED'

            WHERE event_id=?
            """,

            (event_id,)

        )

        conn.commit()

        conn.close()

    def get_event(

        self,

        event_id: str

    ):

        conn = sqlite3.connect(
            self.db_path
        )

        conn.row_factory = (
            sqlite3.Row
        )

        row = conn.execute(

            """
            SELECT *

            FROM events

            WHERE event_id=?
            """,

            (event_id,)

        ).fetchone()

        conn.close()

        if not row:

            return None

        event = dict(row)

        event["payload"] = json.loads(

            event["payload"]

        )

        return event