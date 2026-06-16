from pathlib import Path
import sqlite3


class MigrationRunner:

    def __init__(

        self,

        db_path: str,

        migration_dir: str

    ):

        self.db_path = db_path

        self.migration_dir = (
            Path(migration_dir)
        )

    def run(self):

        conn = sqlite3.connect(
            self.db_path
        )

        files = sorted(

            self.migration_dir.glob(
                "*.sql"
            )

        )

        for file in files:

            with open(

                file,

                "r",

                encoding="utf-8"

            ) as f:

                conn.executescript(
                    f.read()
                )

        conn.commit()

        conn.close()