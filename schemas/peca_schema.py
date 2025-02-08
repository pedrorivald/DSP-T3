from typing import List
from pydantic import BaseModel
from schemas.util_schema import Pagination

class PecaCreate(BaseModel):
  nome: str
  marca: str
  modelo: str
  valor: float

class PecaUpdate(BaseModel):
  nome: str
  marca: str
  modelo: str
  valor: float

class PecaResponse(PecaCreate):
  id: str
    
class PecaPaginatedResponse(BaseModel):
  pagination: Pagination
  pecas: List[PecaResponse]
