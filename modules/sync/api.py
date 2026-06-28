from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query

from infrastructure.database.session import (
    SessionLocal
)

from modules.sync.repository import (
    SyncRepository
)

from modules.sync.schemas import (
    RegisterDeviceRequest,
    PushSyncRequest
)


router = APIRouter(

    prefix="/sync",

    tags=["Sync"]

)


@router.post("/devices/register")
def register_device(
    request: RegisterDeviceRequest
):

    db = SessionLocal()

    try:

        repo = SyncRepository(
            db
        )

        device = repo.register_device(

            merchant_id=
                request.merchant_id,

            device_id=
                request.device_id,

            branch_id=
                request.branch_id,

            user_id=
                request.user_id,

            device_name=
                request.device_name,

            platform=
                request.platform

        )

        return {

            "success":
                True,

            "merchant_id":
                device.merchant_id,

            "device_id":
                device.device_id,

            "status":
                device.status

        }

    except Exception as exc:

        raise HTTPException(

            status_code=400,

            detail=str(
                exc
            )

        )

    finally:

        db.close()


@router.post("/push")
def push_events(
    request: PushSyncRequest
):

    db = SessionLocal()

    try:

        repo = SyncRepository(
            db
        )

        repo.touch_device(

            request.merchant_id,

            request.device_id

        )

        results = []

        for item in request.events:

            record, duplicate = repo.record_client_event(

                merchant_id=
                    request.merchant_id,

                device_id=
                    request.device_id,

                branch_id=
                    request.branch_id,

                client_event_id=
                    item.client_event_id,

                idempotency_key=
                    item.idempotency_key,

                command_name=
                    item.command_name,

                payload=
                    item.payload,

                expected_version=
                    item.expected_version,

                occurred_at=
                    item.occurred_at

            )

            results.append(

                {

                    "client_event_id":
                        item.client_event_id,

                    "status":
                        "DUPLICATE"
                        if duplicate
                        else "RECEIVED",

                    "server_sync_id":
                        record.id
                        if record
                        else None,

                    "error":
                        None

                }

            )

        return {

            "success":
                True,

            "accepted":
                len(
                    results
                ),

            "results":
                results

        }

    except Exception as exc:

        raise HTTPException(

            status_code=400,

            detail=str(
                exc
            )

        )

    finally:

        db.close()


@router.get("/pull/{merchant_id}")
def pull_events(

    merchant_id: str,

    after_event_id: int = Query(
        default=0,
        ge=0
    ),

    limit: int = Query(
        default=100,
        ge=1,
        le=500
    )

):

    db = SessionLocal()

    try:

        repo = SyncRepository(
            db
        )

        events = repo.pull_server_events(

            merchant_id=
                merchant_id,

            after_event_id=
                after_event_id,

            limit=
                limit

        )

        return {

            "merchant_id":
                merchant_id,

            "after_event_id":
                after_event_id,

            "count":
                len(
                    events
                ),

            "events":
                [

                    {

                        "id":
                            event.id,

                        "event_id":
                            event.event_id,

                        "event_type":
                            event.event_type,

                        "merchant_id":
                            event.merchant_id,

                        "aggregate_id":
                            event.aggregate_id,

                        "version":
                            event.version,

                        "payload":
                            event.payload,

                        "previous_hash":
                            event.previous_hash,

                        "current_hash":
                            event.current_hash,

                        "created_at":
                            event.created_at

                    }

                    for event in events

                ]

        }

    except Exception as exc:

        raise HTTPException(

            status_code=400,

            detail=str(
                exc
            )

        )

    finally:

        db.close()


@router.get("/status/{merchant_id}/{device_id}")
def sync_status(

    merchant_id: str,

    device_id: str

):

    db = SessionLocal()

    try:

        repo = SyncRepository(
            db
        )

        return repo.get_device_status(

            merchant_id,

            device_id

        )

    except Exception as exc:

        raise HTTPException(

            status_code=400,

            detail=str(
                exc
            )

        )

    finally:

        db.close()