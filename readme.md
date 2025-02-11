# Rodar no Docker Compose
docker-compose up -d --build

# Parar Containers
docker-compose down

Acessar em http://localhost:8000/docs

# Comandos úteis para desenvolvimento

uvicorn main:app --reload --port 8000

mongodump --uri="mongodb://localhost:27017" --db=oficina --out=C:\Users\Pedro\Documents\workspace\www\DSP-T3\backup
mongorestore --uri="mongodb://localhost:27017" --db=oficina C:\Users\Pedro\Documents\workspace\www\DSP-T3\backup

python -m venv venv

venv\Scripts\activate

pip freeze > requirements.txt

pip install --no-cache-dir -r requirements.txt
