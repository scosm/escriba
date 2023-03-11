from pydantic import BaseModel
from typing import Any, Callable, List, Optional

class Transition(BaseModel):
    name: str  # Unique.
    pattern: str
    state1_name: str
    state2_name: str
    transform: Optional[Callable]  # transform(Situation, Transition) -> Any (data, stored in next Situation's state)
    event: Optional[List[Callable]]
