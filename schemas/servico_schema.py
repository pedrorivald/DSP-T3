from typing import List
from pydantic import BaseModel
from schemas.util_schema import Pagination

class ServicoCreate(BaseModel):
  nome: str
  valor: float
  categoria: str

class ServicoUpdate(BaseModel):
  nome: str
  valor: float
  ativo: bool
  categoria: str

class ServicoResponse(ServicoCreate):
  id: str
  ativo: bool
    
class ServicoPaginatedResponse(BaseModel):
  pagination: Pagination
  servicos: List[ServicoResponse]
