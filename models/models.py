from beanie import Document, Link
from typing import List, Optional
from datetime import datetime


class Peca(Document):
  nome: str
  marca: str
  modelo: str
  valor: float

  class Settings:
    collection = "pecas"


class Servico(Document):
  nome: str
  valor: float
  ativo: bool
  categoria: str

  class Settings:
    collection = "servicos"


class Mecanico(Document):
  nome: str
  sobrenome: str
  telefone: str
  email: Optional[str] = None

  class Settings:
    collection = "mecanicos"


class Cliente(Document):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

  class Settings:
    collection = "clientes"


class OrdemServico(Document):
  cliente: Link[Cliente]
  mecanico: Link[Mecanico]
  servicos: List[Link[Servico]]
  pecas: List[Link[Peca]]
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: float

  class Settings:
    collection = "ordens_servico"
