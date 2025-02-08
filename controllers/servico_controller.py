from fastapi import APIRouter, Query

from repositories.servico_repository import ServicoRepository
from schemas.servico_schema import ServicoCreate, ServicoResponse, ServicoPaginatedResponse, ServicoResponse, ServicoUpdate

router = APIRouter(prefix="/servicos", tags=["Serviços"])
servico_repo = ServicoRepository()

@router.get("/", response_model=ServicoPaginatedResponse)
async def list_servicos(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await servico_repo.list_servicos(page, size)

@router.post("/", response_model=ServicoResponse)
async def create_servico(servico: ServicoCreate):
  return await servico_repo.create_servico(servico)

@router.get("/{id}", response_model=ServicoResponse)
async def get(id: str):
  return await servico_repo.get(id)
  
@router.put("/{id}", response_model=ServicoResponse)
async def update(id: str, servico: ServicoUpdate):
  return await servico_repo.update(id, servico)
  
@router.delete("/{id}")
async def delete(id: str):
  return await servico_repo.delete(id)
