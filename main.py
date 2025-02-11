from fastapi import FastAPI, HTTPException, Request, Response
from controllers import cliente_controller, mecanico_controller, ordem_servico_controller, peca_controller, servico_controller
from db import db
from exceptions.exceptions import BadRequestException, InternalServerErrorException, NotFoundException
from exceptions.global_exception_handler import bad_request_exception_handler, global_exception_handler, http_exception_handler, internal_server_error_exception_handler, not_found_exception_handler
import logging
from datetime import datetime
from beanie import init_beanie

from dotenv import load_dotenv

load_dotenv()

from models.models import Peca, PecasOrdemServico, Servico, Mecanico, Cliente, OrdemServico

app = FastAPI(title="Oficina Mecânica")

@app.on_event("startup")
async def init_db():
  await init_beanie(database=db.db, document_models=[Peca, Servico, Mecanico, Cliente, OrdemServico, PecasOrdemServico])

app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(InternalServerErrorException, internal_server_error_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(cliente_controller.router)
app.include_router(mecanico_controller.router)
app.include_router(peca_controller.router)
app.include_router(servico_controller.router)
app.include_router(ordem_servico_controller.router)

def get_log_level(status_code):
  log_levels = {
    2: logging.INFO,      # 2xx: Sucesso
    3: logging.WARNING,   # 3xx: Redirecionamento
    4: logging.ERROR,     # 4xx: Erro do cliente
    5: logging.CRITICAL,  # 5xx: Erro do servidor
  }
  return log_levels.get(status_code // 100, logging.DEBUG)

@app.middleware("http")
async def log(request: Request, call_next):
  start_time = datetime.now()
  method = request.method
  path = request.url.path

  response: Response = await call_next(request)
  status_code = response.status_code

  log_level = get_log_level(status_code)
  logging.log(log_level, f"Metodo: {method} | Caminho: {path} | Status: {status_code} | Data/Hora: {start_time}")

  return response

@app.get("/")
def root():
  return {"message": "API funcionando corretamente!"}
