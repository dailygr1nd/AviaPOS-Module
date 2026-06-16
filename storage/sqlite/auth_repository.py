import sqlite3


class AuthRepository:

    def __init__(self, db_path: str):

        self.db_path = db_path

    def get_user(self, username: str):

        conn = sqlite3.connect(
            self.db_path
        )

        conn.row_factory = (
            sqlite3.Row
        )

        row = conn.execute(

            """
            SELECT *
            FROM auth_users
            WHERE username = ?
            """,

            (username,)

        ).fetchone()

        conn.close()

        return row