from fastapi import APIRouter, Query

from repositories.peca_repository import PecaRepository
from schemas.peca_schema import PecaCreate, PecaResponse, PecaPaginatedResponse, PecaResponse, PecaUpdate

router = APIRouter(prefix="/pecas", tags=["Pecas"])
peca_repo = PecaRepository()

@router.get("/", response_model=PecaPaginatedResponse)
async def list_pecas(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await peca_repo.list_pecas(page, size)

@router.post("/", response_model=PecaResponse)
async def create_peca(peca: PecaCreate):
  return await peca_repo.create_peca(peca)

@router.get("/{id}", response_model=PecaResponse)
async def get(id: str):
  return await peca_repo.get(id)
  
@router.put("/{id}", response_model=PecaResponse)
async def update(id: str, peca: PecaUpdate):
  return await peca_repo.update(id, peca)
  
@router.delete("/{id}")
async def delete(id: str):
  return await peca_repo.delete(id)
