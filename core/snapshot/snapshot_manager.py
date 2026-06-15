import json

class SnapshotManager:

    def save(

        self,

        path,

        state

    ):

        with open(

            path,

            "w"

        ) as f:

            json.dump(

                state,

                f,

                indent=4

            )

    def load(

        self,

        path

    ):

        with open(

            path,

            "r"

        ) as f:

            return json.load(f)