from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ExerciseType(str, Enum):
    cardio = "Cardio"
    strength = "Strength"
    flexibility = "Flexibility"
    hybrid = "Hybrid"

class ExerciseSession(BaseModel):
    exercise: ExerciseType
    date_created: datetime
    recorded_by: int