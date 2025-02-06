# Desenvolvimento

python -m venv venv

venv\Scripts\activate

pip install fastapi uvicorn pydantic
pip install beanie
pip install motor

pip freeze > requirements.txt

pip install --no-cache-dir -r requirements.txt

uvicorn main:app --reload --port 8000

# Rodar no Docker
`docker build -t dsp-t3 .`
`docker run -d -p 8000:8000 dsp-t3`
Acessar em http://localhost:8000