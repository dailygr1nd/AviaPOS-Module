import json
import sqlite3

from datetime import (
    datetime,
    timezone
)


class ProjectionStore:

    def __init__(

        self,

        db_path: str

    ):

        self.db_path = db_path

    def save(

        self,

        projection_name: str,

        merchant_id: str,

        state: dict

    ):

        conn = sqlite3.connect(
            self.db_path
        )

        conn.execute(

            """
            INSERT OR REPLACE
            INTO projections (

                projection_name,

                merchant_id,

                projection_data,

                updated_at

            )

            VALUES (?, ?, ?, ?)
            """,

            (

                projection_name,

                merchant_id,

                json.dumps(state),

                datetime.now(
                    timezone.utc
                ).isoformat()

            )

        )

        conn.commit()

        conn.close()

    def load(

        self,

        projection_name: str,

        merchant_id: str

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
            from projectionss
            WHERE projection_name = ?
            AND merchant_id = ?
            """,

            (

                projection_name,

                merchant_id

            )

        ).fetchone()

        conn.close()

        if not row:

            return None

        return json.loads(

            row["projection_data"]

        )