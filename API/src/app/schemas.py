from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class URLCreate(BaseModel):
    original_url: str
    prefix: Optional[str] = None

class URLResponse(BaseModel):
    original_url: str
    short_url: str
    click_count: int
    activation_date: datetime
    expiration_date: datetime

    class Config:
        from_attributes = True