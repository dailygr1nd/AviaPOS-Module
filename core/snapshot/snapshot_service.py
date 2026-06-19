import json
import sqlite3


class SnapshotService:

    def __init__(

        self,

        db_path: str

    ):

        self.db_path = db_path

    def save(

        self,

        merchant_id: str,

        aggregate_state: dict,

        event_count: int

    ):

        conn = sqlite3.connect(

            self.db_path

        )

        conn.execute(

            """
            INSERT OR REPLACE INTO snapshots(

                merchant_id,
                event_count,
                state

            )

            VALUES(?,?,?)
            """,

            (

                merchant_id,

                event_count,

                json.dumps(
                    aggregate_state
                )

            )

        )

        conn.commit()

        conn.close()

    def load(

        self,

        merchant_id: str

    ):

        conn = sqlite3.connect(

            self.db_path

        )

        row = conn.execute(

            """
            SELECT state

            FROM snapshots

            WHERE merchant_id=?
            """,

            (merchant_id,)

        ).fetchone()

        conn.close()

        if not row:

            return None

        return json.loads(

            row[0]

        )