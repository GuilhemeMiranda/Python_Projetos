# Modulo principal: main.py
"""
Módulo principal: main.py
Ponto de entrada da aplicação FastAPI.
Responsável por:
- Inicializar o app
- Configurar o banco de dados
- Importar e registrar as rotas
- Criar as tabelas (se não existirem)
"""

from fastapi import FastAPI
from app.database import Base, engine
from app.routes import veiculos, usuarios, manutencoes, planos


# ============================================================
# 1. Criação das tabelas do banco
# ============================================================
# O SQLAlchemy cria automaticamente todas as tabelas
# definidas em models.py se elas ainda não existirem.
Base.metadata.create_all(bind=engine)

# ============================================================
# 2. Inicialização do aplicativo FastAPI
# ============================================================
app = FastAPI(
    title="API - Minha Manutenção Veicular",
    description="Sistema para cadastro e controle de manutenção de veículos.",
    version="1.0.0"
)

# ============================================================
# 3. Registro das rotas
# ============================================================
# Aqui adicionamos o módulo de veículos
app.include_router(veiculos.router)
# Aqui adicionamos o módulo de usuários
app.include_router(usuarios.router)
# Aqui adicionamos o módulo de manutenções
app.include_router(manutencoes.router)
# Aqui adicionamos o módulo de planos de manutenção
app.include_router(planos.router)

# ============================================================
# 4. Rota inicial (opcional)
# ============================================================
@app.get("/")
def home():
    """
    Endpoint inicial de boas-vindas.
    """
    return {"mensagem": "Bem-vindo à API de Manutenção Veicular 🚗"}
