from typing import List, Optional
from pydantic import BaseModel
from schemas.cliente_schema import ClienteResponse
from schemas.mecanico_schema import MecanicoResponse
from schemas.util_schema import Pagination
from datetime import datetime

class OrdemServicoPecaCreate(BaseModel):
  quantidade: int
  peca_id: str
  
class OrdemServicoCreate(BaseModel):
  cliente_id: str
  mecanico_id: str

class OrdemServicoUpdate(BaseModel):
  cliente_id: str
  mecanico_id: str

class OrdemServicoResponse(BaseModel):
  id: str
  cliente_id: str
  mecanico_id: str
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: Optional[float] = None

class OrdemServicoPartialResponse(BaseModel):
  id: str
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: Optional[float] = None
  
  cliente: ClienteResponse
  mecanico: MecanicoResponse
    
class OrdemServicoPaginatedResponse(BaseModel):
  pagination: Pagination
  ordens_servicos: List[OrdemServicoPartialResponse]
    
class OrdemServicoServicoResponse(BaseModel):
  id: str
  nome: str
  valor: float
  categoria: str
  
class OrdemServicoPecaResponse(BaseModel):
  id: str
  nome: str
  marca: str
  modelo: str
  valor: float
  quantidade: int
    
class OrdemServicoFullResponse(BaseModel):
  id: str
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: Optional[float] = None
  
  cliente: ClienteResponse
  mecanico: MecanicoResponse
  
  servicos: List[OrdemServicoServicoResponse]
  pecas: List[OrdemServicoPecaResponse]

