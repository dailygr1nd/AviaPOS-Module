from fastapi import APIRouter
from fastapi import HTTPException

from core.audit.chain_verifier import (
    ChainVerifier
)

from infrastructure.database.session import (
    SessionLocal
)

from infrastructure.event_store.repository import (
    EventRepository
)


router = APIRouter()


@router.get(
    "/integrity/merchant/{merchant_id}"
)
def verify_merchant_chain(
    merchant_id: str
):

    db = SessionLocal()

    try:

        repo = EventRepository(
            db
        )

        events = repo.get_by_merchant_ordered(
            merchant_id
        )

        return ChainVerifier.verify_merchant_chain(
            events
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(
                exc
            )

        )

    finally:

        db.close()


@router.get(
    "/integrity/aggregate/{merchant_id}/{aggregate_id}"
)
def verify_aggregate_integrity(

    merchant_id: str,

    aggregate_id: str

):

    db = SessionLocal()

    try:

        repo = EventRepository(
            db
        )

        events = repo.get_by_aggregate_ordered(

            merchant_id,

            aggregate_id

        )

        return ChainVerifier.verify_event_integrity(
            events
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(
                exc
            )

        )

    finally:

        db.close()