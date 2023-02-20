from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class AudioFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    duration: Optional[int]
    bpm: Optional[int]
    created_at: datetime
    updated_at: datetime


class AudioFileCreate(SQLModel):
    name: str
    duration: Optional[int]
    bpm: Optional[int]


class AudioPID(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    process_id: str
    created_at: datetime
    updated_at: datetime