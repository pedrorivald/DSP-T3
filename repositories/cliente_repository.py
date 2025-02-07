from typing import Optional
from datetime import datetime
from models.models import Cliente
from schemas.cliente_schema import ClienteCreate, ClientePaginatedResponse
from schemas.util_schema import Pagination

class ClienteRepository:
  
  async def create_cliente(self, data: ClienteCreate):
    cliente = Cliente(**data.model_dump())
    await cliente.insert()
    return cliente
  
  async def list_clientes(self, page: int = 1, size: int = 10):
    total = await Cliente.find_all().count()
    clientes = await Cliente.find_all().skip((page - 1) * size).limit(size).to_list()
    
    return ClientePaginatedResponse(
      clientes=[cliente.to_dict() for cliente in clientes],
      pagination=Pagination(
        page=page,
        size=size,
        total=total
      )
    )