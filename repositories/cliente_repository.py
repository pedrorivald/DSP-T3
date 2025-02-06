from typing import Optional
from datetime import datetime
from models.models import Cliente

class ClienteRepository:
  
  async def create_cliente(self, cliente: Cliente):
    await cliente.insert()
    return cliente
  
  async def list_clientes(self, page: int = 1, size: int = 10):
    total = await Cliente.find_all().count()
    clientes = await Cliente.find_all().skip((page - 1) * size).limit(size).to_list()
    
    return {
      "resultado": clientes, 
      "paginacao": {
        "page": page, 
        "size": size, 
        "total": total
      }
    }