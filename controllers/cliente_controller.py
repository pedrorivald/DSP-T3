from fastapi import APIRouter, Query

from repositories.cliente_repository import ClienteRepository
from schemas.cliente_schema import ClienteCreate, ClienteCreateResponse, ClientePaginatedResponse, ClienteResponse, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_repo = ClienteRepository()

@router.get("/", response_model=ClientePaginatedResponse)
async def list_clientes(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await cliente_repo.list_clientes(page, size)

@router.post("/", response_model=ClienteCreateResponse)
async def create_cliente(cliente: ClienteCreate):
  return await cliente_repo.create_cliente(cliente)

@router.get("/{id}", response_model=ClienteResponse)
async def get(id: str):
  return await cliente_repo.get(id)
  
@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update(id: str, cliente: ClienteUpdate):
  return await cliente_repo.update(id, cliente)
  
@router.delete("/{id}")
async def delete(id: str):
  return await cliente_repo.delete(id)
