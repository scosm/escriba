from pydantic import BaseModel
from typing import Any, Callable, List, Optional

class State(BaseModel):
    name: str
    end: bool
    data: Optional[Any]
    transform: Optional[Callable]
    event: Optional[List[Callable]]