from typing import Optional
from fastapi import APIRouter, Depends, Query
from models.models import Cliente, Mecanico, OrdemServico
from repositories.ordem_servico_repository import OrdemServicoRepository
from schemas.ordem_servico_schema import OrdemServicoCreate, OrdemServicoFullResponse, OrdemServicoPaginatedResponse, OrdemServicoPecaCreate, OrdemServicoResponse, OrdemServicoUpdate
from datetime import datetime

router = APIRouter(prefix="/ordens_servicos", tags=["Ordens de Serviços"])
ordem_servico_repo = OrdemServicoRepository()
    
@router.post("/", response_model=OrdemServicoResponse)
async def create(ordem_servico: OrdemServicoCreate):
  return await ordem_servico_repo.create(ordem_servico)

@router.get("/", response_model=OrdemServicoPaginatedResponse)
async def list(
  page: int = Query(1, alias="page"), 
  size: int = Query(10, alias="size"),
  mecanico_id: Optional[str] = Query(None, alias="mecanico_id"),
  cliente_id: Optional[str] = Query(None, alias="cliente_id"),
  nome_mecanico: Optional[str] = Query(None, alias="nome_mecanico"),
  nome_cliente: Optional[str] = Query(None, alias="nome_cliente"),
  data_abertura_inicio: Optional[datetime] = Query(None, alias="data_abertura_inicio"),
  data_abertura_fim: Optional[datetime] = Query(None, alias="data_abertura_fim") 
):
  
  ordens_servicos = await ordem_servico_repo.list(
    page=page, 
    size=size, 
    mecanico_id=mecanico_id, 
    cliente_id=cliente_id, 
    nome_mecanico=nome_mecanico, 
    nome_cliente=nome_cliente, 
    data_abertura_inicio=data_abertura_inicio, 
    data_abertura_fim=data_abertura_fim
  )

  return ordens_servicos

@router.get("/{id}", response_model=OrdemServicoFullResponse)
async def get(id: str):
  return await ordem_servico_repo.get(id)
  
@router.put("/{id}", response_model=OrdemServicoResponse)
async def update(id: str, ordem_servico: OrdemServicoUpdate):
  return await ordem_servico_repo.update(id, ordem_servico)

@router.delete("/{id}")
async def delete(id: str):
  return await ordem_servico_repo.delete(id)
  
@router.patch("/{id}/concluir")
async def conclude(id: str):
  return await ordem_servico_repo.conclude(id)

@router.delete("/{id}/pecas/{peca_id}")
async def remove_peca(id: str, peca_id: str):
  return await ordem_servico_repo.remove_peca(id, peca_id)

@router.delete("/{id}/servicos/{servico_id}")
async def remove_servico(id: str, servico_id: str):
  return await ordem_servico_repo.remove_servico(id, servico_id)

@router.post("/{id}/pecas")
async def add_peca(id: str, peca: OrdemServicoPecaCreate):
  return await ordem_servico_repo.add_peca(id, peca)

@router.post("/{id}/servicos")
async def add_servico(id: str, servico_id: str):
  return await ordem_servico_repo.add_servico(id, servico_id)