from typing import Literal
from pydantic import BaseModel

class GradeAnswer(BaseModel):
    answer_found: Literal["yes", "no"]