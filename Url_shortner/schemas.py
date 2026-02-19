from pydantic import BaseModel, HttpUrl
from typing import Optional

class ShortenRequest(BaseModel):
    url: HttpUrl
    alias: Optional[str] = None   # NEW

class ShortenResponse(BaseModel):
    code: str
    short_url: str
    original_url: str

class StatsResponse(BaseModel):
    code: str
    original_url: str
    short_url: str
    clicks: int
    created_at: str


