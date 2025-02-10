from typing import List
from pydantic import BaseModel
from schemas.util_schema import Pagination

class ClienteCreate(BaseModel):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

class ClienteUpdate(BaseModel):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

class ClienteResponse(ClienteCreate):
  id: str
  
class ClienteCreateResponse(ClienteResponse):
  id: str
    
class ClientePaginatedResponse(BaseModel):
  pagination: Pagination
  clientes: List[ClienteResponse]
