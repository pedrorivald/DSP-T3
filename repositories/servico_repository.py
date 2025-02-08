from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Servico, OrdemServico
from schemas.servico_schema import ServicoCreate, ServicoPaginatedResponse, ServicoUpdate
from schemas.util_schema import Pagination

class ServicoRepository:
  
  async def create_servico(self, data: ServicoCreate):
    servico_data = data.model_dump()
    servico_data["ativo"] = True
    
    servico = Servico(**servico_data)
    await servico.insert()
    return servico.to_dict()
  
  async def list_servicos(self, page: int = 1, size: int = 10):
    total = await Servico.find_all().count()
    servicos = await Servico.find_all().skip((page - 1) * size).limit(size).to_list()
    
    return ServicoPaginatedResponse(
      servicos=[servico.to_dict() for servico in servicos],
      pagination=Pagination(
        page=page,
        size=size,
        total=total
      )
    )
    
  async def get(self, id: str):
    servico = await Servico.get(id)
    if not servico:
      raise NotFoundException(f"Serviço com id {id} não encontrado.")
        
    return servico.to_dict()

  async def update(self, id: str, data: ServicoUpdate):
    servico = await Servico.get(id)
    
    if servico:
      update_data = data.model_dump(exclude_unset=True)
      await servico.set(update_data)
    else:
      raise NotFoundException(f"Serviço com id {id} não encontrado.")
    
    return servico.to_dict()

  async def delete(self, id: str):
    servico = await Servico.get(id)
    if not servico:
      raise NotFoundException(f"Serviço com id {id} não encontrado.")
      
    servico_is_related = await OrdemServico.find_one({"servicos": servico.id})
    if servico_is_related:
      raise BadRequestException(f"Serviço com id {id} está relacionado a uma ordem de serviço.")  
    
    await servico.delete()
    return {"message": "Serviço excluído com sucesso"}