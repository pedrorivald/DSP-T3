from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Peca, OrdemServico
from schemas.peca_schema import PecaCreate, PecaPaginatedResponse, PecaUpdate
from schemas.util_schema import Pagination

class PecaRepository:
  
  async def create_peca(self, data: PecaCreate):
    peca = Peca(**data.model_dump())
    await peca.insert()
    return peca.to_dict()
  
  async def list_pecas(self, page: int = 1, size: int = 10):
    total = await Peca.find_all().count()
    pecas = await Peca.find_all().skip((page - 1) * size).limit(size).to_list()
    
    return PecaPaginatedResponse(
      pecas=[peca.to_dict() for peca in pecas],
      pagination=Pagination(
        page=page,
        size=size,
        total=total
      )
    )
    
  async def get(self, id: str):
    peca = await Peca.get(id)
    if not peca:
      raise NotFoundException(f"Peça com id {id} não encontrada.")
        
    return peca.to_dict()

  async def update(self, id: str, data: PecaUpdate):
    peca = await Peca.get(id)
    
    if peca:
      update_data = data.model_dump(exclude_unset=True)
      await peca.set(update_data)
    else:
      raise NotFoundException(f"Peça com id {id} não encontrada.")
    
    return peca.to_dict()

  async def delete(self, id: str):
    peca = await Peca.get(id)
    if not peca:
      raise NotFoundException(f"Peça com id {id} não encontrada.")
      
    peca_is_related = await OrdemServico.find_one({"pecas": peca.id})
    if peca_is_related:
      raise BadRequestException(f"Peça com id {id} está relacionada a uma ordem de serviço.")  
    
    await peca.delete()
    return {"message": "Peça excluída com sucesso"}