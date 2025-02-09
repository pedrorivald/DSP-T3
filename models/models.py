from beanie import Document, Link
from typing import List, Optional
from datetime import datetime

from bson import ObjectId

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
    collection = "pecas"


class Servico(BaseDocument):
  nome: str
  valor: float
  ativo: bool
  categoria: str

  class Settings:
    collection = "servicos"


class Mecanico(BaseDocument):
  nome: str
  sobrenome: str
  telefone: str
  email: Optional[str] = None

  class Settings:
    collection = "mecanicos"


class Cliente(BaseDocument):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

  class Settings:
    collection = "clientes"
    

class PecasOrdemServico(BaseDocument):
  peca: Link[Peca]
  quantidade: int
  
  class Settings:
    collection = "pecas_ordens_servicos"


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
    collection = "ordens_servico"
