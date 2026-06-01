from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class PriorityEnum(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class StatusEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


# Area Schemas
class AreaBase(BaseModel):
    name: str
    description: Optional[str] = None


class AreaCreate(AreaBase):
    pass


class AreaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class AreaResponse(AreaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    description: str
    priority: PriorityEnum = PriorityEnum.MEDIUM
    status: StatusEnum = StatusEnum.OPEN
    date_raised: datetime
    date_closed: Optional[datetime] = None


class TaskCreate(BaseModel):
    area_id: int
    description: str
    priority: PriorityEnum = PriorityEnum.MEDIUM
    date_raised: datetime


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    date_raised: Optional[datetime] = None
    date_closed: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: int
    area_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AreaWithTasks(AreaResponse):
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True


# Statistics Schema
class TaskStats(BaseModel):
    total: int
    open: int
    closed: int
    critical: int
