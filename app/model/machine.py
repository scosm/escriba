from pydantic import BaseModel
from typing import Any, Callable, Dict, List
from app.model.state import State
from app.model.transition import Transition

class Machine(BaseModel):
    # Maps state_name to set of Transitions (each having the source and destination states).
    # The key to the inner dict is the name (unique) of the transition.
    graph: Dict[str, Dict[str, Transition]]
    states: Dict[str, State]
