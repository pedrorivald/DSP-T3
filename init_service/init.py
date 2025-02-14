import asyncio
from datetime import timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from faker import Faker
from models.models import Endereco, Peca, Servico, Mecanico, Cliente, PecasOrdemServico, OrdemServico

fake = Faker("pt_BR")

async def connect():
  client = AsyncIOMotorClient("mongodb://oficina-mongodb:27017/oficina")
  db = client.get_database()
  await init_beanie(db, document_models=[Peca, Servico, Mecanico, Cliente, PecasOrdemServico, OrdemServico])

async def init_data():
  print("Inicializando o banco de dados com dados fakes")
  # Cria Peças
  print("Criando peças")
  pecas = []
  for _ in range(12):
    peca = Peca(
      nome=fake.word().capitalize(),
      marca=fake.company(),
      modelo=fake.word(),
      valor=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
    )
    await peca.insert()
    pecas.append(peca)
    print(peca)

  # Cria Serviços
  print("Criando serviços")
  servicos = []
  categorias = ["Manutenção", "Pneu", "Relação", "Suspensão", "BikeFit", "Limpeza"]
  for _ in range(7):
    servico = Servico(
      nome=fake.word().capitalize(),
      valor=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
      ativo=fake.boolean(chance_of_getting_true=80),
      categoria=fake.random_element(elements=categorias)
    )
    await servico.insert()
    servicos.append(servico)
    print(servico)

  # Cria dados para Mecanico
  print("Criando mecanicos")
  mecanicos = []
  for _ in range(5):
    mecanico = Mecanico(
      nome=fake.first_name(),
      sobrenome=fake.last_name(),
      telefone=fake.phone_number(),
      email=fake.email()
    )
    await mecanico.insert()
    mecanicos.append(mecanico)
    print(mecanico)

  # Cria dados para Cliente
  print("Criando clientes")
  clientes = []
  for _ in range(33):
    cliente = Cliente(
      nome=fake.first_name(),
      sobrenome=fake.last_name(),
      endereco=Endereco(
        cidade=fake.city(),
        logradouro=f"{fake.street_address()}, {fake.postcode()}",
        bairro=fake.neighborhood()
      ),
      telefone=fake.phone_number()
    )
    await cliente.insert()
    clientes.append(cliente)
    print(cliente)

  # Cria itens de peças para ordem de serviço
  print("Criando peças para ordens de serviço")
  pecas_ordens_servicos = []
  for _ in range(10):
    peca_escolhida = fake.random_element(elements=pecas)
    item = PecasOrdemServico(
      peca=peca_escolhida.to_ref(),
      quantidade=fake.random_int(min=1, max=5)
    )
    await item.insert()
    pecas_ordens_servicos.append(item)
    print(item)

  # Cria ordens de serviço
  print("Criando ordens de serviço")
  for _ in range(34):
    cliente_escolhido = fake.random_element(elements=clientes)
    mecanico_escolhido = fake.random_element(elements=mecanicos)
    
    # Seleciona aleatoriamente alguns serviços e itens de peças para essa ordem:
    selected_servicos = fake.random_elements(elements=servicos, length=fake.random_int(min=1, max=3), unique=True)
    servicos_refs = [s.to_ref() for s in selected_servicos]

    selected_itens_peca = fake.random_elements(elements=pecas_ordens_servicos, length=fake.random_int(min=0, max=2), unique=True)
    pecas_refs = [item.to_ref() for item in selected_itens_peca]
    
    # Calcula o total de peças (valor da peça x quantidade)
    total_pecas = 0.0
    for item in selected_itens_peca:
      # Busca a peça relacionada
      peca: Peca = await item.peca.fetch()
      total_pecas += peca.valor * item.quantidade

    # Calcula o total dos serviços (soma dos valores)
    total_servicos = sum(s.valor for s in selected_servicos)

    # Valor total da ordem
    total_ordem = round(total_pecas + total_servicos, 2)
    
    data_abertura = fake.date_time_this_year(before_now=True, after_now=False)
    # Define data_conclusao com 75% de chance
    data_conclusao = data_abertura + timedelta(days=fake.random_int(min=1, max=10)) if fake.boolean(chance_of_getting_true=75) else None
    
    ordem = OrdemServico(
      cliente=cliente_escolhido.to_ref(),
      mecanico=mecanico_escolhido.to_ref(),
      servicos=servicos_refs,
      pecas=pecas_refs,
      data_abertura=data_abertura,
      data_conclusao=data_conclusao,
      situacao="concluida" if data_conclusao else "pendente",
      valor=total_ordem if data_conclusao else None
    )
    await ordem.insert()
    print(ordem)

async def main():
  try:
    await connect()
    await init_data()
    print("Banco inicializado com sucesso.")
  except Exception:
    print(Exception)

if __name__ == "__main__":
  asyncio.run(main())