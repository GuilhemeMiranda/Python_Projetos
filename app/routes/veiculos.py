from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import get_db
from app import models, schemas, security

router = APIRouter()

def get_usuario_id_from_token(request: Request, db: Session) -> int:
    """
    Extrai o ID do usuário a partir do token JWT no cookie.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )
    
    usuario_data = security.verificar_token_seguro(token)
    if not usuario_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    usuario_id = usuario_data.get("sub")
    
    # Se 'sub' for email, busca o ID do usuário no banco
    if usuario_id and not str(usuario_id).isdigit():
        result = db.execute(
            text("SELECT id FROM usuarios WHERE email = :email"),
            {"email": usuario_id}
        ).fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        usuario_id = result[0]
    
    return int(usuario_id)

@router.post("/", response_model=schemas.Veiculo, status_code=status.HTTP_201_CREATED)
def criar_veiculo(
    veiculo: schemas.VeiculoCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Cria um novo veículo e associa ao usuário logado.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Verifica se já existe veículo com essa placa
    veiculo_existente = db.query(models.Veiculo).filter(
        models.Veiculo.placa == veiculo.placa
    ).first()
    
    if veiculo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um veículo cadastrado com essa placa"
        )
    
    # Cria o novo veículo
    db_veiculo = models.Veiculo(
        placa=veiculo.placa,
        ano=veiculo.ano,
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        km_atual=veiculo.km_atual,
        usuario_id=usuario_id
    )
    
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    
    return db_veiculo

@router.get("/", response_model=List[schemas.Veiculo])
def listar_veiculos(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todos os veículos do usuário logado.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    veiculos = db.query(models.Veiculo).filter(
        models.Veiculo.usuario_id == usuario_id
    ).offset(skip).limit(limit).all()
    
    return veiculos

@router.get("/{veiculo_id}", response_model=schemas.Veiculo)
def obter_veiculo(
    veiculo_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Obtém um veículo específico do usuário logado.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    veiculo = db.query(models.Veiculo).filter(
        models.Veiculo.id == veiculo_id,
        models.Veiculo.usuario_id == usuario_id
    ).first()
    
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    return veiculo

@router.put("/{veiculo_id}", response_model=schemas.Veiculo)
def atualizar_veiculo(
    veiculo_id: int,
    veiculo: schemas.VeiculoCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Atualiza um veículo do usuário logado.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    db_veiculo = db.query(models.Veiculo).filter(
        models.Veiculo.id == veiculo_id,
        models.Veiculo.usuario_id == usuario_id
    ).first()
    
    if not db_veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    # Atualiza os campos
    db_veiculo.placa = veiculo.placa
    db_veiculo.ano = veiculo.ano
    db_veiculo.marca = veiculo.marca
    db_veiculo.modelo = veiculo.modelo
    db_veiculo.km_atual = veiculo.km_atual
    
    db.commit()
    db.refresh(db_veiculo)
    
    return db_veiculo

@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_veiculo(
    veiculo_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Deleta um veículo do usuário logado.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    db_veiculo = db.query(models.Veiculo).filter(
        models.Veiculo.id == veiculo_id,
        models.Veiculo.usuario_id == usuario_id
    ).first()
    
    if not db_veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    db.delete(db_veiculo)
    db.commit()
    
    return None
