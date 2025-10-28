#Módulo: routes/usuarios.py
#Define as rotas relacionadas à entidade Usuário.
#Permite criar, listar e buscar usuários.


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db

# ============================================================
# 1. Inicialização do roteador
# ============================================================

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

# ============================================================
# 2. Endpoint: Criar novo usuário
# ============================================================

@router.post("/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário.
    - Requer: nome, email e senha.
    - O e-mail deve ser único.
    """
    usuario_existente = crud.buscar_usuario_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    novo_usuario = crud.criar_usuario(db, usuario)
    return novo_usuario


# ============================================================
# 3. Endpoint: Listar usuários
# ============================================================

@router.get("/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Retorna todos os usuários cadastrados.
    """
    return crud.listar_usuarios(db)


# ============================================================
# 4. Endpoint: Buscar usuário por e-mail
# ============================================================

@router.get("/buscar", response_model=schemas.UsuarioResponse)
def buscar_usuario(email: str, db: Session = Depends(get_db)):
    """
    Busca um usuário pelo e-mail.
    Exemplo de uso: /usuarios/buscar?email=teste@exemplo.com
    """
    usuario = crud.buscar_usuario_por_email(db, email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario
