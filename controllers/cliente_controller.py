from fastapi import APIRouter, Query

from repositories.cliente_repository import ClienteRepository
from schemas.cliente_schema import ClienteCreate, ClienteCreateResponse, ClientePaginatedResponse, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_repo = ClienteRepository()

@router.get("/", response_model=ClientePaginatedResponse)
async def list_clientes(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await cliente_repo.list_clientes(page, size)

@router.post("/", response_model=ClienteCreateResponse)
async def create_cliente(cliente: ClienteCreate):
  result = await cliente_repo.create_cliente(cliente)
  return result.to_dict()
