from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ExerciseType(str, Enum):
    cardio = "Cardio"
    strength = "Strength"
    flexibility = "Flexibility"
    hybrid = "Hybrid"

# Key learning point:
# Each attribute of a Pydantic model has a type.
# But that type can itself be another Pydantic model.
# In this case, the ExerciseSession model has an attribute exercise of type ExerciseType.

class ExerciseSession(BaseModel):
    exercise: ExerciseType
    date_created: datetime
    recorded_by: int