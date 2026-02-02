from pydantic import BaseModel, Field
from typing import Optional

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed for book creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new Book",
                "author": "Name of the Author",
                "description": "Summary ro description about the book.",
                "rating": 5
            }
        }
    }