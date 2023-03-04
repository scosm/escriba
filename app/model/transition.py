from pydantic import BaseModel
from typing import Any, Callable, List, Optional

class Transition(BaseModel):
    name: str  # Unique.
    pattern: str
    state1_name: str
    state2_name: str
    data: Optional[Any]
    transform: Optional[Callable]
    event: Optional[List[Callable]]
