import sqlite3


def bootstrap():

    conn = sqlite3.connect(

        "storage/sqlite/aviapos.db"

    )

    conn.execute(

        """
        CREATE TABLE IF NOT EXISTS events (

            event_id TEXT PRIMARY KEY,

            merchant_id TEXT,

            event_type TEXT,

            timestamp TEXT,

            previous_hash TEXT,

            payload_hash TEXT,

            event_hash TEXT,

            payload TEXT,

            sync_status TEXT
        )
        """
    )

    conn.commit()

    conn.close()


if __name__ == "__main__":

    bootstrap()