from typing import List
from pydantic import BaseModel
from schemas.util_schema import Pagination

class Endereco(BaseModel):
  cidade: str
  bairro: str
  logradouro: str

class ClienteCreate(BaseModel):
  nome: str
  sobrenome: str
  endereco: Endereco
  telefone: str

class ClienteUpdate(BaseModel):
  nome: str
  sobrenome: str
  endereco: Endereco
  telefone: str

class ClienteResponse(ClienteCreate):
  id: str
  
class ClienteCreateResponse(ClienteResponse):
  id: str
    
class ClientePaginatedResponse(BaseModel):
  pagination: Pagination
  clientes: List[ClienteResponse]
