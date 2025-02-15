from typing import List, Optional
from pydantic import BaseModel
from schemas.util_schema import Pagination

class MecanicoCreate(BaseModel):
  nome: str
  sobrenome: str
  email: Optional[str] = None
  telefone: str

class MecanicoUpdate(BaseModel):
  nome: str
  sobrenome: str
  email: Optional[str] = None
  telefone: str

class MecanicoResponse(MecanicoCreate):
  id: str
    
class MecanicoPaginatedResponse(BaseModel):
  pagination: Pagination
  mecanicos: List[MecanicoResponse]
