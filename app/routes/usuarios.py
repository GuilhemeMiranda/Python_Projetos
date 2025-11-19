#Módulo: routes/usuarios.py
#Define as rotas relacionadas à entidade Usuário.
#Permite criar, listar e buscar usuários.


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

# ============================================================
# Inicialização do roteador
# ============================================================

router = APIRouter()  # SEM prefix aqui

# ============================================================
# Rotas de Usuários
# ============================================================

@router.post("/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário."""
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.create_usuario(db=db, usuario=usuario)

@router.get("/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os usuários."""
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtém um usuário específico por ID."""
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario
