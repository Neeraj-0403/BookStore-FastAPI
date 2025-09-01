from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class BookEntity:
    id: Optional[int] = None
    title: Optional[str]  = None
    author: Optional[str]  = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None