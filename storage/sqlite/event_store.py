import json
import sqlite3

from typing import List
from typing import Optional


class EventStore:

    def __init__(

        self,

        db_path: str = "storage/sqlite/aviapos.db"

    ):

        self.db_path = db_path

    def _connect(self):

        conn = sqlite3.connect(

            self.db_path

        )

        conn.row_factory = sqlite3.Row

        return conn

    def append(

        self,

        event

    ):

        conn = self._connect()

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

        conn = self._connect()

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

    def load_events(

        self,

        merchant_id: str

    ) -> List[dict]:

        return self.replay_events(

            merchant_id

        )

    def latest_hash(

        self,

        merchant_id: str

    ) -> str:

        conn = self._connect()

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

        if row is None:

            return "GENESIS"

        return row["event_hash"]

    def count_events(

        self,

        merchant_id: str

    ) -> int:

        conn = self._connect()

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

        conn = self._connect()

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

    def mark_synced(

        self,

        event_id: str

    ):

        conn = self._connect()

        conn.execute(

            """
            UPDATE events

            SET sync_status = 'SYNCED'

            WHERE event_id = ?
            """,

            (event_id,)

        )

        conn.commit()

        conn.close()


    def load_events(
        self,
        merchant_id: str
):
        return self.replay_events(
        merchant_id
    )

    def get_event(

        self,

        event_id: str

    ) -> Optional[dict]:

        conn = self._connect()

        row = conn.execute(

            """
            SELECT *

            FROM events

            WHERE event_id = ?
            """,

            (event_id,)

        ).fetchone()

        conn.close()

        if row is None:

            return None

        event = dict(row)

        event["payload"] = json.loads(

            event["payload"]

        )

        return event