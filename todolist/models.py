from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy import Column, String, TIMESTAMP, Text, Boolean
from sqlalchemy.sql import func

from conf.db import Base


class ToDoList(Base):
    __tablename__ = 'todolist'

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=True)
    lead_time = Column(TIMESTAMP(timezone=True),
                       nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())