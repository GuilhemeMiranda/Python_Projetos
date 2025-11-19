from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app import models, schemas, security

router = APIRouter()

def get_usuario_id_from_token(request: Request, db: Session) -> int:
    """Extrai o ID do usuário a partir do token JWT no cookie."""
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

@router.post("/", response_model=schemas.VeiculoResponse, status_code=status.HTTP_201_CREATED)
def criar_veiculo(
    veiculo_data: schemas.VeiculoCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria um novo veículo vinculado ao usuário logado."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Verifica se a placa já existe para este usuário
    existing = db.execute(
        text("SELECT id FROM veiculos WHERE placa = :placa AND usuario_id = :usuario_id"),
        {"placa": veiculo_data.placa, "usuario_id": usuario_id}
    ).fetchone()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um veículo com esta placa"
        )
    
    # Insere o novo veículo
    db.execute(
        text("""
            INSERT INTO veiculos (placa, ano, marca, modelo, km_atual, usuario_id)
            VALUES (:placa, :ano, :marca, :modelo, :km_atual, :usuario_id)
        """),
        {
            "placa": veiculo_data.placa,
            "ano": veiculo_data.ano,
            "marca": veiculo_data.marca,
            "modelo": veiculo_data.modelo,
            "km_atual": veiculo_data.km_atual,
            "usuario_id": usuario_id
        }
    )
    db.commit()
    
    # Busca o veículo criado
    result = db.execute(
        text("SELECT * FROM veiculos WHERE placa = :placa AND usuario_id = :usuario_id"),
        {"placa": veiculo_data.placa, "usuario_id": usuario_id}
    ).fetchone()
    
    return result

@router.get("/", response_model=List[dict])
def listar_veiculos(
    request: Request,
    db: Session = Depends(get_db),
    placa: Optional[str] = None
):
    """Lista todos os veículos do usuário logado."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    query = "SELECT * FROM veiculos WHERE usuario_id = :usuario_id"
    params = {"usuario_id": usuario_id}
    
    if placa:
        query += " AND placa LIKE :placa"
        params["placa"] = f"%{placa}%"
    
    query += " ORDER BY placa"
    
    result = db.execute(text(query), params).fetchall()
    
    veiculos = []
    for row in result:
        veiculos.append({
            "id": row[0],
            "placa": row[1],
            "ano": row[2],
            "marca": row[3],
            "modelo": row[4],
            "km_atual": row[5],
            "usuario_id": row[6]
        })
    
    return veiculos

@router.get("/{veiculo_id}", response_model=dict)
def obter_veiculo(
    veiculo_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém um veículo específico."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    result = db.execute(
        text("SELECT * FROM veiculos WHERE id = :id AND usuario_id = :usuario_id"),
        {"id": veiculo_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    return {
        "id": result[0],
        "placa": result[1],
        "ano": result[2],
        "marca": result[3],
        "modelo": result[4],
        "km_atual": result[5],
        "usuario_id": result[6]
    }

@router.put("/{veiculo_id}", response_model=dict)
def atualizar_veiculo(
    veiculo_id: int,
    veiculo_data: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza um veículo existente (exceto a placa)."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Verifica se o veículo existe e pertence ao usuário
    existing = db.execute(
        text("SELECT id FROM veiculos WHERE id = :id AND usuario_id = :usuario_id"),
        {"id": veiculo_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    # Atualiza os dados (sem alterar a placa)
    db.execute(
        text("""
            UPDATE veiculos 
            SET marca = :marca, modelo = :modelo, ano = :ano, km_atual = :km_atual
            WHERE id = :id AND usuario_id = :usuario_id
        """),
        {
            "id": veiculo_id,
            "usuario_id": usuario_id,
            "marca": veiculo_data.get("marca"),
            "modelo": veiculo_data.get("modelo"),
            "ano": veiculo_data.get("ano"),
            "km_atual": veiculo_data.get("km_atual")
        }
    )
    db.commit()
    
    # Retorna o veículo atualizado
    result = db.execute(
        text("SELECT * FROM veiculos WHERE id = :id"),
        {"id": veiculo_id}
    ).fetchone()
    
    return {
        "id": result[0],
        "placa": result[1],
        "ano": result[2],
        "marca": result[3],
        "modelo": result[4],
        "km_atual": result[5],
        "usuario_id": result[6]
    }

@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_veiculo(
    veiculo_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Deleta um veículo."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Verifica se o veículo existe e pertence ao usuário
    existing = db.execute(
        text("SELECT id FROM veiculos WHERE id = :id AND usuario_id = :usuario_id"),
        {"id": veiculo_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    # Delete o veículo
    db.execute(
        text("DELETE FROM veiculos WHERE id = :id AND usuario_id = :usuario_id"),
        {"id": veiculo_id, "usuario_id": usuario_id}
    )
    db.commit()
    
    return None
