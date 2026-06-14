from pydantic import BaseModel
from datetime import datetime


class ApiResponse(BaseModel):

    success: bool

    message: str | None = None


class EventResponse(BaseModel):

    success: bool

    event_id: str