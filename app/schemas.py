from pydantic import BaseModel
from typing import Optional

class PostIn(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True