from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Mecanico, OrdemServico
from schemas.mecanico_schema import MecanicoCreate, MecanicoPaginatedResponse, MecanicoUpdate
from schemas.util_schema import Pagination

class MecanicoRepository:
  
  async def create_mecanico(self, data: MecanicoCreate):
    mecanico = Mecanico(**data.model_dump())
    await mecanico.insert()
    return mecanico.to_dict()
  
  async def list_mecanicos(self, page: int = 1, size: int = 10):
    total = await Mecanico.find_all().count()
    mecanicos = await Mecanico.find_all().skip((page - 1) * size).limit(size).to_list()
    
    return MecanicoPaginatedResponse(
      mecanicos=[mecanico.to_dict() for mecanico in mecanicos],
      pagination=Pagination(
        page=page,
        size=size,
        total=total
      )
    )
    
  async def get(self, id: str):
    mecanico = await Mecanico.get(id)
    if not mecanico:
      raise NotFoundException(f"Mecanico com id {id} não encontrado.")
        
    return mecanico.to_dict()

  async def update(self, id: str, data: MecanicoUpdate):
    mecanico = await Mecanico.get(id)
    
    if mecanico:
      update_data = data.model_dump(exclude_unset=True)
      await mecanico.set(update_data)
    else:
      raise NotFoundException(f"Mecanico com id {id} não encontrado.")
    
    return mecanico.to_dict()

  async def delete(self, id: str):
    mecanico = await Mecanico.get(id)
    if not mecanico:
      raise NotFoundException(f"Mecanico com id {id} não encontrado.")
      
    mecanico_is_related = await OrdemServico.find_one({"mecanico": mecanico.id})
    if mecanico_is_related:
      raise BadRequestException(f"Mecanico com id {id} está relacionado a uma ordem de serviço.")  
    
    await mecanico.delete()
    return {"message": "Mecanico excluído com sucesso"}