from typing import Optional

from bson import ObjectId
from fastapi import HTTPException
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Cliente, Endereco, Mecanico, OrdemServico, Peca, PecasOrdemServico, Servico
from datetime import datetime, timezone

from schemas.cliente_schema import ClienteResponse
from schemas.mecanico_schema import MecanicoResponse
from schemas.ordem_servico_schema import OrdemServicoCreate, OrdemServicoFullResponse, OrdemServicoPaginatedResponse, OrdemServicoPartialResponse, OrdemServicoPecaResponse, OrdemServicoResponse, OrdemServicoServicoResponse, OrdemServicoUpdate
from schemas.peca_schema import PecaResponse
from schemas.servico_schema import ServicoResponse
from schemas.util_schema import Pagination

class OrdemServicoRepository:

  async def create(self, data: OrdemServicoCreate):
    # Verificar se o cliente existe
    cliente = await Cliente.get(data.cliente_id)
    if not cliente:
      raise NotFoundException(f"Cliente com id {id} não encontrado.")
    
    # Verificar se o mecanico existe
    mecanico = await Mecanico.get(data.mecanico_id)
    if not mecanico:
      raise NotFoundException(f"Mecânico com id {id} não encontrado.")
          
    ordem_servico = OrdemServico(
      cliente=cliente.id, 
      mecanico=mecanico.id,
      data_abertura = datetime.now(timezone.utc),
      situacao = "pendente",
      data_conclusao = None,
      valor = None
    )
    
    await ordem_servico.insert()
    
    return OrdemServicoResponse(
      id=str(ordem_servico.id),
      cliente_id=str(cliente.id),
      mecanico_id=str(mecanico.id),
      data_abertura=ordem_servico.data_abertura,
      data_conclusao=ordem_servico.data_conclusao,
      situacao=ordem_servico.situacao,
      valor=ordem_servico.valor
    )

  async def list(
    self,
    page: int = 1,
    size: int = 10,
    mecanico_id: Optional[str] = None,
    cliente_id: Optional[str] = None,
    nome_mecanico: Optional[str] = None,
    nome_cliente: Optional[str] = None,
    data_abertura_inicio: Optional[datetime] = None,
    data_abertura_fim: Optional[datetime] = None,
  ):
    query = {}

    if mecanico_id:
      query["mecanico._id"] = ObjectId(mecanico_id)
    if cliente_id:
      query["cliente._id"] = ObjectId(cliente_id)
    if nome_mecanico:
      query["mecanico.nome"] = {"$regex": nome_mecanico, "$options": "i"}
    if nome_cliente:
      query["cliente.nome"] = {"$regex": nome_cliente, "$options": "i"}
    if data_abertura_inicio and data_abertura_fim:
      query["data_abertura"] = {"$gte": data_abertura_inicio, "$lte": data_abertura_fim}

    total = await OrdemServico.find(query, fetch_links=True).count()
    ordens = await OrdemServico.find(query, fetch_links=True).skip((page - 1) * size).limit(size).to_list()

    return OrdemServicoPaginatedResponse(
      ordens_servicos=[OrdemServicoPartialResponse(
        id=str(ordem.id),
        cliente=ordem.cliente.to_dict(),
        mecanico=ordem.mecanico.to_dict(),
        data_abertura=ordem.data_abertura,
        data_conclusao=ordem.data_conclusao,
        situacao=ordem.situacao,
        valor=ordem.valor,
      ) for ordem in ordens],
      pagination=Pagination(
        page=page,
        size=size,
        total=total
      )
    )
    
  async def get(self, id: str):      
    data = await OrdemServico.get(id, fetch_links=True)
      
    if not data:
      raise NotFoundException("Ordem de serviço não encontrada.")      
        
    return OrdemServicoFullResponse(
      id=str(data.id),
      cliente=ClienteResponse(
        id=str(data.cliente.id), 
        nome=data.cliente.nome, 
        sobrenome=data.cliente.sobrenome,
        endereco=Endereco(
          cidade=data.cliente.endereco.cidade,
          bairro=data.cliente.endereco.bairro,
          logradouro=data.cliente.endereco.logradouro
        ), 
        telefone=data.cliente.telefone
      ),
      mecanico=MecanicoResponse(
        id=str(data.mecanico.id), 
        nome=data.mecanico.nome, 
        sobrenome=data.mecanico.sobrenome,
        telefone=data.mecanico.telefone, 
        email=data.mecanico.email
      ),
      servicos=[
        OrdemServicoServicoResponse(
          id=str(s.id), 
          nome=s.nome, 
          valor=s.valor, 
          categoria=s.categoria
        ) for s in data.servicos],
      pecas=[
        OrdemServicoPecaResponse(
          id=str(item.peca.id), 
          nome=item.peca.nome, 
          marca=item.peca.marca, 
          modelo=item.peca.modelo, 
          valor=item.peca.valor,
          quantidade=item.quantidade
        ) for item in data.pecas],
      data_abertura=data.data_abertura,
      data_conclusao=data.data_conclusao,
      situacao=data.situacao,
      valor=data.valor
    )

  async def update(self, id: str, data: OrdemServicoUpdate):
    ordem_servico = await OrdemServico.get(id, fetch_links=True)
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "concluida":
      raise BadRequestException("Ordem de serviço já foi concluida.")
    
    cliente = await Cliente.get(data.cliente_id)
    if not cliente:
      raise NotFoundException(f"Cliente com id {id} não encontrado.")
    
    mecanico = await Mecanico.get(data.mecanico_id)
    if not mecanico:
      raise NotFoundException(f"Mecânico com id {id} não encontrado.")
    
    ordem_servico.cliente = cliente
    ordem_servico.mecanico = mecanico
    
    await ordem_servico.save()
    
    return OrdemServicoResponse(
      id=str(ordem_servico.id),
      cliente_id=str(cliente.id),
      mecanico_id=str(mecanico.id),
      data_abertura=ordem_servico.data_abertura,
      data_conclusao=ordem_servico.data_conclusao,
      situacao=ordem_servico.situacao,
      valor=ordem_servico.valor
    )
      
  async def delete(self, id: str):
    ordem_servico = await OrdemServico.get(id)
    if ordem_servico:
      await ordem_servico.delete()
      return {"message": "ordem de Serviço excluída com sucesso"}
    else:
      raise NotFoundException("Ordem de serviço não encontrada.")

  async def conclude(self, id: str):
    ordem_servico = await OrdemServico.get(id)
    
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "concluida":
      raise BadRequestException("Ordem de serviço já foi concluida.")
    
    pipeline = [
      {"$match": {"_id": id}},
      {"$lookup": {
        "from": "servicos",
        "localField": "servicos",
        "foreignField": "_id",
        "as": "servicos_info"
      }},
      {"$unwind": "$pecas"},  # Desestrutura a lista de peças para processar uma por uma
      {"$lookup": {
        "from": "pecas",
        "localField": "pecas.peca",
        "foreignField": "_id",
        "as": "peca_info"
      }},
      {"$unwind": "$peca_info"},
      {"$project": {
        "total_servicos": {"$sum": "$servicos_info.valor"},
        "total_pecas": {"$sum": {"$multiply": ["$peca_info.valor", "$pecas.quantidade"]}}
      }},
      {"$group": {
        "_id": "$_id",
        "valor_total": {"$sum": ["$total_servicos", "$total_pecas"]}
      }}
    ]

    result = await OrdemServico.aggregate(pipeline).to_list()
    if not result:
      raise HTTPException(status_code=500, detail="Erro ao calcular total")

    valor_total = result[0]["valor_total"]

    # Atualiza a ordem no banco
    await OrdemServico.find_one({"_id": id}).update({
      "$set": {
        "situacao": "concluida",
        "data_conclusao": datetime.now(timezone.utc),
        "valor": valor_total
      }
    })

    return { "message": "Ordem de serviço concluída com sucesso", "valor_total": valor_total }

  async def remove_servico(self, id: str, servico_id: str):
    ordem_servico = await OrdemServico.get(id, fetch_links=True)
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "concluida":
      raise BadRequestException("Ordem de serviço já foi concluida.")
    
    servico = await Servico.get(servico_id)
    if not servico:
      raise NotFoundException("Serviço não encontrado.")
    
    # Remove o serviço pelo ID
    ordem_servico.servicos = [s for s in ordem_servico.servicos if str(s.id) != servico_id]
    await ordem_servico.save()
    
    return { "message": "Serviço removido da ordem de serviço." }

  async def add_servico(self, id: str, servico_id: str):
    ordem_servico = await OrdemServico.get(id, fetch_links=True)
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "concluida":
      raise BadRequestException("Ordem de serviço já foi concluida.")
    
    servico = await Servico.get(servico_id)
    if not servico:
      raise NotFoundException("Serviço não encontrado.")
    
    # Verifica se o serviço já existe na ordem
    servico_existente = next((s for s in ordem_servico.servicos if str(s.id) == servico_id), None)
    
    if servico_existente:
      raise BadRequestException("Serviço já existe na ordem de serviço")
    else:
      ordem_servico.servicos.append(servico)
      await ordem_servico.save()
      return { "message": "Serviço adicionado na ordem de serviço." }
    
  async def add_peca(self, id: str, data: any):
    ordem_servico = await OrdemServico.get(id, fetch_links=True)
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "concluida":
      raise BadRequestException("Ordem de serviço já foi concluida.")
    
    peca = await Peca.get(data.peca_id)
    if not peca:
      raise NotFoundException("Peça não encontrada.")
    
    # Verifica se a peça já existe na ordem
    peca_existente = next((item for item in ordem_servico.pecas if str(item.peca.id) == data.peca_id), None)
    
    if peca_existente:
      peca_existente.quantidade += data.quantidade
      ordem_servico_peca = await PecasOrdemServico.get(peca_existente.id, fetch_links=True)
      ordem_servico_peca.quantidade = peca_existente.quantidade
      await ordem_servico_peca.save()
    else:
      ordem_servico_peca = PecasOrdemServico(peca=peca.id, quantidade=data.quantidade)
      await ordem_servico_peca.insert()
      ordem_servico.pecas.append(ordem_servico_peca)
      await ordem_servico.save()
    
    return { "message": "Peça adicionada na ordem de serviço." }

  async def remove_peca(self, id: str, peca_id: str):
    ordem_servico = await OrdemServico.get(id, fetch_links=True)
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "concluida":
      raise BadRequestException("Ordem de serviço já foi concluida.")
    
    peca = await Peca.get(peca_id)
    if not peca:
      raise NotFoundException("Peça não encontrada.")
    
    ordem_servico.pecas = [item for item in ordem_servico.pecas if str(item.peca.id) != peca_id]
    await ordem_servico.save()
    
    return { "message": "Peça removida da ordem de serviço." }