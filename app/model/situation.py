from pydantic import BaseModel
from typing import Optional
from app.model.machine import Machine

class Situation(BaseModel):
    id: str  # Unique.
    input_complete: str
    input_remainder: str
    state_name: str
    machine: Machine
    history: Optional[list]  # Previous situations (as dict) of this trail.

