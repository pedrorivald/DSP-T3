from datetime import datetime, timedelta, timezone
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from exceptions.exceptions import InternalServerErrorException, NotFoundException
from models.models import Mecanico, OrdemServico
from repositories.mecanico_repository import MecanicoRepository
from schemas.mecanico_schema import MecanicoCreate, MecanicoPaginatedResponse, MecanicoResponse, MecanicoUpdate

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import uuid

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])
mecanico_repo = MecanicoRepository()

@router.get("/", response_model=MecanicoPaginatedResponse)
async def list_mecanicos(page: int = Query(1, alias="page"), size: int = Query(10, alias="size")):
  return await mecanico_repo.list_mecanicos(page, size)

@router.post("/", response_model=MecanicoResponse)
async def create_mecanico(mecanico: MecanicoCreate):
  return await mecanico_repo.create_mecanico(mecanico)
  
@router.put("/{mecanico_id}", response_model=MecanicoResponse)
async def update(id: str, mecanico: MecanicoUpdate):
  return await mecanico_repo.update(id, mecanico)
  
@router.delete("/{id}")
async def delete(id: str):
  return await mecanico_repo.delete(id)

@router.get("/report")
async def report_mecanicos(data_inicio: str, data_fim: str):
  data_inicio_convert = datetime.strptime(data_inicio, "%d/%m/%Y")
  data_inicio_datetime = datetime(data_inicio_convert.year, data_inicio_convert.month, data_inicio_convert.day, 0, 0, 0)
  
  data_fim_convert = datetime.strptime(data_fim, "%d/%m/%Y")
  data_fim_datetime = datetime(data_fim_convert.year, data_fim_convert.month, data_fim_convert.day, 23, 59, 59)
  
  pipeline = [
    # Filtra as ordens com data_abertura dentro do período desejado
    {
      "$match": {
        "data_abertura": {
          "$gte": data_inicio_datetime,
          "$lte": data_fim_datetime
        }
      }
    },
    # Projeta um campo auxiliar "mecanico_id" extraindo o "$id" do DBRef armazenado em "mecanico"
    {
      "$project": {
        "mecanico_id": "$mecanico.$id",
        "data_abertura": 1
      }
    },
    # Agrupa as ordens pelo campo "mecanico_id" e conta quantas ordens cada mecânico possui
    {
      "$group": {
        "_id": "$mecanico_id", 
        "total_ordens": {"$sum": 1}
      }
    },
    # Ordena os grupos em ordem decrescente pelo total de ordens
    { 
     "$sort": { "total_ordens": -1 } 
    },
    # Realiza o lookup para buscar os dados do mecânico na coleção "mecanicos"
    {
      "$lookup": {
        "from": "mecanicos",           # nome da coleção de mecânicos
        "localField": "_id",           # "mecanico_id" (agora um ObjectId)
        "foreignField": "_id",         # campo _id na coleção de mecânicos
        "as": "mecanico_info"
      }
    },
    # Desestrutura o array gerado pelo lookup para obter um único documento do mecânico
    { "$unwind": "$mecanico_info" },
    # Projeta os campos desejados: nome, sobrenome e total de ordens
    {
      "$project": {
        "_id": 0,
        "nome": "$mecanico_info.nome",
        "sobrenome": "$mecanico_info.sobrenome",
        "total_ordens": 1
      }
    }
  ]
    
  report = await OrdemServico.aggregate(pipeline).to_list()
  
  if len(report) < 1:
    return { "message": "Sem dados" }
  
  try:
    filename = generate_report(report, data_inicio, data_fim)
  except Exception as e:
    raise InternalServerErrorException(f"Erro ao gerar PDF: {str(e)}")
  
  url_report = f"http://localhost:8000/mecanicos/reports/download/{filename}"
  
  return {
    "report": report, 
    "url_report": url_report
  }
    
@router.get("/reports/download/{filename}")
async def download_report(filename: str):
  filepath = os.path.join("reports", filename)
  if not os.path.exists(filepath):
    raise NotFoundException("Relatório não encontrado")
  
  return FileResponse(
    filepath, 
    media_type="application/pdf", 
    filename=filename
  )

@router.get("/{id}", response_model=MecanicoResponse)
async def get(id: str):
  return await mecanico_repo.get(id)

def generate_report(data, data_inicio, data_fim):
  
  data_geracao = datetime.now(timezone.utc)
  
  # Gera um nome único para o PDF
  filename = f"{uuid.uuid4()}.pdf"
  filepath = os.path.join("reports", filename)
  
  # Cria o diretório 'reports' se não existir
  os.makedirs("reports", exist_ok=True)
  
  doc = SimpleDocTemplate(filepath, pagesize=A4)
  elementos = []
  
  styles = getSampleStyleSheet()
  
  titulo = Paragraph("<b>Relatório de Mecânicos</b>", styles["Title"])
  elementos.append(titulo)
  elementos.append(Spacer(1, 12))
  
  info = f"Data de geração: {data_geracao} <br/> Período: {data_inicio} a {data_fim}"
  elementos.append(Paragraph(info, styles["Normal"]))
  elementos.append(Spacer(1, 12))
  
  dados_tabela = [["Nome", "Sobrenome", "Total de Ordens"]]
  
  for i, item in enumerate(data):
    linha = [item["nome"], item["sobrenome"], item["total_ordens"]]
    dados_tabela.append(linha)
  
  tabela = Table(dados_tabela, colWidths=[150, 150, 100])
  
  estilo = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
  ])
  
  for i in range(1, len(dados_tabela)):
    if i % 2 == 0:
      estilo.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
  
  tabela.setStyle(estilo)
  elementos.append(tabela)
  
  doc.build(elementos)
  
  return filename