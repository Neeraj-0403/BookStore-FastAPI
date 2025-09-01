from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title:str
    author:str
    description:Optional[str] =None

class BookUpdate(BaseModel):
    title:Optional[str]=None
    author: Optional[str]=None
    description:Optional[str]=None

class BookRead(BaseModel):
    id:int
    title:str
    author:str
    description:Optional[str]
    created_at:datetime

    model_config={
        "from_attributes":True
    }