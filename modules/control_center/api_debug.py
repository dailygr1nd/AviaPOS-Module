from fastapi import APIRouter

from modules.control_center.debug import rebuild_projections

router = APIRouter()


@router.post("/debug/rebuild")
def rebuild():

    return rebuild_projections()