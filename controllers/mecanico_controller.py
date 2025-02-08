from fastapi import APIRouter, Query

from repositories.mecanico_repository import MecanicoRepository
from schemas.mecanico_schema import MecanicoCreate, MecanicoCreateResponse, MecanicoPaginatedResponse, MecanicoResponse, MecanicoUpdate

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])
mecanico_repo = MecanicoRepository()

@router.get("/", response_model=MecanicoPaginatedResponse)
async def list_mecanicos(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await mecanico_repo.list_mecanicos(page, size)

@router.post("/", response_model=MecanicoCreateResponse)
async def create_mecanico(mecanico: MecanicoCreate):
  return await mecanico_repo.create_mecanico(mecanico)

@router.get("/{id}", response_model=MecanicoResponse)
async def get(id: str):
  return await mecanico_repo.get(id)
  
@router.put("/{mecanico_id}", response_model=MecanicoResponse)
async def update(id: str, mecanico: MecanicoUpdate):
  return await mecanico_repo.update(id, mecanico)
  
@router.delete("/{id}")
async def delete(id: str):
  return await mecanico_repo.delete(id)
