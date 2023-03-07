from pydantic import BaseModel
from app.model.machine import Machine
from app.model.state import State

class Situation(BaseModel):
    id: str  # Unique.
    input_complete: str
    input_remainder: str
    state: State
    machine: Machine
    history: list  # Previous situations (as Situations) of this trail. Cannot use List[Situation], because of a circular reference: undefined Situation.

