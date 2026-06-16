import sqlite3


class UnitOfWork:

    def __init__(

        self,

        db_path: str

    ):

        self.db_path = db_path

        self.conn = None

    def __enter__(self):

        self.conn = sqlite3.connect(

            self.db_path

        )

        return self
    def commit(self):

        self.conn.commit()

    def rollback(self):

        self.conn.rollback()

    def __exit__(

        self,

        exc_type,

        exc_val,

        exc_tb

    ):

        if exc_type:

            self.rollback()

        else:

            self.commit()

        self.conn.close()