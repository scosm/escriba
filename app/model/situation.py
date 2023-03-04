from pydantic import BaseModel
from app.model.machine import Machine

class Situation(BaseModel):
    id: str  # Unique.
    input_complete: str
    input_remainder: str
    state_name: str
    machine: Machine

