from storage.sqlite.projection_store import (
    ProjectionStore
)

class ProjectionManager:

    def __init__(

        self,

        db_path

    ):

        self.store = (
            ProjectionStore(
                db_path
            )
        )

    def persist(

        self,

        projection_name,

        merchant_id,

        projection

    ):

        state = {}

        if hasattr(

            projection,

            "__dict__"

        ):

            state = (
                projection.__dict__
            )

        self.store.save(

            projection_name,

            merchant_id,

            state
        )

    def restore(

        self,

        projection_name,

        merchant_id

    ):

        return self.store.load(

            projection_name,

            merchant_id
        )