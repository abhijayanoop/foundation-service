from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from typing import Literal
from datetime import datetime

class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class UploadSource(BaseModel):
    source: Literal["upload"]
    file_id: str

class UrlSource(BaseModel):
    source: Literal["url"]
    url: str = Field(pattern=r"^https?://")

class RawTextSource(BaseModel):
    source: Literal["raw_text"]
    text: str = Field(min_length=0, max_length=100_000)

Source = UploadSource | UrlSource | RawTextSource

class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    source: Source
    metadata: dict[str, str | int | bool] = Field(default_factory=dict)

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: str):
        if not v.strip():
            raise ValueError("title cannot be white spaces")
        return v.strip()

    @model_validator(mode="after")
    def metadata_within_limit(self) -> "DocumentCreate":
        if(len(self.metadata)>20):
            raise ValueError("metadata cannot be more than 20 keys")
        self.metadata = {k.strip().lower(): v for k, v in self.metadata.items()}
        return self

class DocumentOut(BaseModel):
    id: str
    title: str
    status: str
    createdAt: datetime
    
