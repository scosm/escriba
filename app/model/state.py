from pydantic import BaseModel
from typing import Any, Callable, List, Optional

class State(BaseModel):
    name: str
    start: bool
    end: bool
    data: Optional[Any]  # Destination storage location for result of the preceding transition's transform function.
    process: Optional[Callable]
    event: Optional[List[Callable]]