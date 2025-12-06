from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import date
from app.database import get_db
from app import security

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

@router.get("/", response_model=List[dict])
def listar_veiculos_planos(
    request: Request,
    db: Session = Depends(get_db)
):
    """Lista todos os planos associados aos veículos do usuário logado."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    query = """
        SELECT 
            vp.id,
            vp.veiculo_id,
            vp.plano_manutencao_id,
            v.placa,
            v.marca,
            v.modelo,
            p.nome as plano_nome,
            vp.proxima_manutencao_data,
            vp.proxima_manutencao_km,
            vp.ativo
        FROM veiculos_planos vp
        INNER JOIN veiculos v ON vp.veiculo_id = v.id
        INNER JOIN planos_manutencao p ON vp.plano_manutencao_id = p.id
        WHERE v.usuario_id = :usuario_id
        ORDER BY v.placa, p.nome
    """
    
    result = db.execute(text(query), {"usuario_id": usuario_id}).fetchall()
    
    associacoes = []
    for row in result:
        # Trata a data que pode vir como string ou objeto date
        proxima_data = row[7]
        if proxima_data:
            if isinstance(proxima_data, str):
                proxima_data_iso = proxima_data
            else:
                proxima_data_iso = proxima_data.isoformat()
        else:
            proxima_data_iso = None
        
        associacoes.append({
            "id": row[0],
            "veiculo_id": row[1],
            "plano_id": row[2],
            "veiculo_placa": row[3],
            "veiculo_modelo": f"{row[4]} {row[5]}",
            "plano_nome": row[6],
            "proxima_data": proxima_data_iso,
            "proximo_km": row[8],
            "ativo": row[9]
        })
    
    return associacoes

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_veiculo_plano(
    dados: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    """Associa um plano a um veículo."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    veiculo_id = dados.get("veiculo_id")
    plano_id = dados.get("plano_id")
    proxima_data = dados.get("proxima_data")
    proximo_km = dados.get("proximo_km")
    
    # Verifica se o veículo existe e pertence ao usuário
    veiculo = db.execute(
        text("SELECT id, placa, marca, modelo FROM veiculos WHERE id = :id AND usuario_id = :usuario_id"),
        {"id": veiculo_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    # Verifica se o plano existe e pertence ao usuário
    plano = db.execute(
        text("SELECT id, nome FROM planos_manutencao WHERE id = :id AND usuario_id = :usuario_id"),
        {"id": plano_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano não encontrado"
        )
    
    # Verifica se já existe associação
    existe = db.execute(
        text("""
            SELECT id FROM veiculos_planos 
            WHERE veiculo_id = :veiculo_id AND plano_manutencao_id = :plano_id
        """),
        {"veiculo_id": veiculo_id, "plano_id": plano_id}
    ).fetchone()
    
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este plano já está associado ao veículo"
        )
    
    # Cria a associação
    db.execute(
        text("""
            INSERT INTO veiculos_planos 
            (veiculo_id, plano_manutencao_id, data_inicio, proxima_manutencao_data, proxima_manutencao_km, ativo)
            VALUES (:veiculo_id, :plano_id, :data_inicio, :proxima_data, :proximo_km, :ativo)
        """),
        {
            "veiculo_id": veiculo_id,
            "plano_id": plano_id,
            "data_inicio": date.today(),
            "proxima_data": proxima_data,
            "proximo_km": proximo_km,
            "ativo": True
        }
    )
    db.commit()
    
    # Busca a associação criada
    nova = db.execute(
        text("""
            SELECT vp.id, vp.proxima_manutencao_data, vp.proxima_manutencao_km
            FROM veiculos_planos vp
            WHERE vp.veiculo_id = :veiculo_id AND vp.plano_manutencao_id = :plano_id
        """),
        {"veiculo_id": veiculo_id, "plano_id": plano_id}
    ).fetchone()
    
    # Trata a data
    proxima_data_retorno = nova[1]
    if proxima_data_retorno:
        if isinstance(proxima_data_retorno, str):
            proxima_data_retorno = proxima_data_retorno
        else:
            proxima_data_retorno = proxima_data_retorno.isoformat()
    
    return {
        "id": nova[0],
        "veiculo_id": veiculo_id,
        "plano_id": plano_id,
        "veiculo_placa": veiculo[1],
        "veiculo_modelo": f"{veiculo[2]} {veiculo[3]}",
        "plano_nome": plano[1],
        "proxima_data": proxima_data_retorno,
        "proximo_km": nova[2],
        "ativo": True
    }

@router.delete("/{veiculo_plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_veiculo_plano(
    veiculo_plano_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Remove a associação de um plano com um veículo."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Verifica se a associação existe e o veículo pertence ao usuário
    existe = db.execute(
        text("""
            SELECT vp.id 
            FROM veiculos_planos vp
            INNER JOIN veiculos v ON vp.veiculo_id = v.id
            WHERE vp.id = :id AND v.usuario_id = :usuario_id
        """),
        {"id": veiculo_plano_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação não encontrada"
        )
    
    # Remove a associação
    db.execute(
        text("DELETE FROM veiculos_planos WHERE id = :id"),
        {"id": veiculo_plano_id}
    )
    db.commit()
    
    return None