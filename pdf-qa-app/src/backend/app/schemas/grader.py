from typing import Literal
from pydantic import BaseModel

class GradeDocuments(BaseModel):
    binary_score: Literal["yes", "no"]