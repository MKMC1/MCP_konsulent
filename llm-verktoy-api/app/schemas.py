from pydantic import BaseModel
from typing import List

class KonsulentOut(BaseModel):
    navn: str
    tilgjengelighet: str

class SammendragOut(BaseModel):
    sammendrag: str
    konsulenter: List[KonsulentOut]
