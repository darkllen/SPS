from pydantic import BaseModel
from enum import Enum
from typing import Optional

class EventName(str, Enum):
    UNLOCKED = 'unlocked'
    LOCKED = 'locked'

class EventStatus(str, Enum):
    AVAILABLE = 'available'
    IN_USAGE = 'in_usage'

name_status_map = {
    EventName.LOCKED : EventStatus.IN_USAGE,
    EventName.UNLOCKED : EventStatus.AVAILABLE
}

class SensorEventMessage(BaseModel):
    id: int
    city: str
    event_name: EventName
    user_id: Optional[int]