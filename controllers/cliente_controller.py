from fastapi import APIRouter, Query

from models.models import Cliente
from repositories.cliente_repository import ClienteRepository

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_repo = ClienteRepository()

@router.get("/")
async def list_clientes(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await cliente_repo.list_clientes(page, size)

@router.post("/")
async def create_cliente(cliente: Cliente):
  return await cliente_repo.create_cliente(cliente)
