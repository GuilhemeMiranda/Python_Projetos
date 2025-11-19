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

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import security


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

# montar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# incluir routers existentes
from app.routes import veiculos, usuarios, manutencoes, planos
from app.routes import auth  # rotas de autenticação

# Registra os routers
app.include_router(veiculos.router, prefix="/veiculos", tags=["veiculos"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(manutencoes.router, prefix="/manutencoes", tags=["manutencoes"])
app.include_router(planos.router, prefix="/planos", tags=["planos"])
app.include_router(auth.router, tags=["auth"])

# Função helper para obter usuário do token
def _get_user_from_request(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            return None
        user = security.verificar_token_seguro(token)
        return user
    except Exception:
        # evita 500 se a verificação falhar
        return None

# Rota raiz - redireciona para login ou dashboard
@app.get("/", include_in_schema=False)
def root(request: Request):
    user = _get_user_from_request(request)
    if not user:
        return RedirectResponse("/ui/login")
    return RedirectResponse("/ui/dashboard")

# Rota de login
@app.get("/ui/login", include_in_schema=False)
def ui_login(request: Request):
    # Se já estiver logado, redireciona para dashboard
    user = _get_user_from_request(request)
    if user:
        return RedirectResponse("/ui/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})

# Dashboard (tela inicial com menu)
@app.get("/ui/dashboard", include_in_schema=False)
def ui_dashboard(request: Request):
    user = _get_user_from_request(request)
    if not user:
        return RedirectResponse("/ui/login")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# Tela de cadastro de veículo
@app.get("/ui/veiculo", include_in_schema=False)
def ui_veiculo(request: Request):
    user = _get_user_from_request(request)
    if not user:
        return RedirectResponse("/ui/login")
    return templates.TemplateResponse("veiculo_form.html", {"request": request, "user": user})

# Tela de cadastro de manutenção
@app.get("/ui/manutencao", include_in_schema=False)
def ui_manutencao(request: Request):
    user = _get_user_from_request(request)
    if not user:
        return RedirectResponse("/ui/login")
    return templates.TemplateResponse("manutencao_form.html", {"request": request, "user": user})

# Tela de relatório de manutenções
@app.get("/ui/manutencoes", include_in_schema=False)
def ui_manutencoes(request: Request):
    user = _get_user_from_request(request)
    if not user:
        return RedirectResponse("/ui/login")
    return templates.TemplateResponse("manutencao_report.html", {"request": request, "user": user})

@app.get("/health")
def health_check():
    return {"status": "ok"}
