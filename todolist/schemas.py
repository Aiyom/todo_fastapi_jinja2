from datetime import datetime
from typing import List

from pydantic import BaseModel


class ToDoListSchema(BaseModel):
    id: str | None = None
    title: str
    description: str
    status: bool = True
    lead_time: datetime | None = None
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ToDoListResponse(BaseModel):
    status: str
    results: int
    notes: List[ToDoListSchema]