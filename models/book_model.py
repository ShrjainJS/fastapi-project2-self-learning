from pydantic import BaseModel, Field
from typing import Optional

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, le=5)