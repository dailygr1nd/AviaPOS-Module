import json
import uuid

from datetime import (
    datetime
)

class CheckpointEngine:

    def create_checkpoint(

        self,

        merchant_id,

        projection_name,

        state

    ):

        return {

            "checkpoint_id":

                str(uuid.uuid4()),

            "merchant_id":

                merchant_id,

            "projection_name":

                projection_name,

            "snapshot_data":

                json.dumps(
                    state
                ),

            "created_at":

                datetime.utcnow()
                .isoformat()
        }