from beanie import Document, Link
from typing import List, Optional
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel

class BaseDocument(Document):
  def to_dict(self):
    """Converte ObjectId para string em qualquer documento Beanie."""
    data = self.model_dump()
    if isinstance(self.id, ObjectId):
      data["id"] = str(self.id)
    return data


class Peca(BaseDocument):
  nome: str
  marca: str
  modelo: str
  valor: float

  class Settings:
    name = "pecas"


class Servico(BaseDocument):
  nome: str
  valor: float
  ativo: bool
  categoria: str

  class Settings:
    name = "servicos"


class Mecanico(BaseDocument):
  nome: str
  sobrenome: str
  telefone: str
  email: Optional[str] = None

  class Settings:
    name = "mecanicos"
    
class Endereco(BaseModel):
  cidade: str
  bairro: str
  logradouro: str


class Cliente(BaseDocument):
  nome: str
  sobrenome: str
  endereco: Endereco
  telefone: str

  class Settings:
    name = "clientes"
    

class PecasOrdemServico(BaseDocument):
  peca: Link[Peca]
  quantidade: int
  
  class Settings:
    name = "pecas_ordens_servicos"


class OrdemServico(BaseDocument):
  cliente: Link[Cliente]
  mecanico: Link[Mecanico]
  servicos: Optional[List[Link[Servico]]] = []
  pecas: Optional[List[Link[PecasOrdemServico]]] = []
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: Optional[float] = None

  class Settings:
    name = "ordens_servico"
