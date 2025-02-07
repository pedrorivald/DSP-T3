from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Cliente, OrdemServico
from schemas.cliente_schema import ClienteCreate, ClientePaginatedResponse, ClienteUpdate
from schemas.util_schema import Pagination

class ClienteRepository:
  
  async def create_cliente(self, data: ClienteCreate):
    cliente = Cliente(**data.model_dump())
    await cliente.insert()
    return cliente.to_dict()
  
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
    
  async def get(self, id: str):
    cliente = await Cliente.get(id)
    if not cliente:
      raise NotFoundException(f"Cliente com id {id} não encontrado.")
        
    return cliente.to_dict()

  async def update(self, id: str, data: ClienteUpdate):
    cliente = await Cliente.get(id)
    
    if cliente:
      update_data = data.model_dump(exclude_unset=True)
      await cliente.set(update_data)
    else:
      raise NotFoundException(f"Cliente com id {id} não encontrado.")
    
    return cliente.to_dict()

  async def delete(self, id: str):
    cliente = await Cliente.get(id)
    if not cliente:
      raise NotFoundException(f"Cliente com id {id} não encontrado.")
      
    cliente_is_related = await OrdemServico.find_one({"cliente": cliente.id})
    if cliente_is_related:
      raise BadRequestException(f"Cliente com id {id} está relacionado a uma ordem de serviço.")  
    
    await cliente.delete()
    return {"message": "Cliente excluído com sucesso"}