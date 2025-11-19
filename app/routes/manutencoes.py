#Módulo: routes/manutencoes.py
#Define as rotas para cadastro, listagem e gerenciamento de manutenções.

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.database import get_db
from app import models, schemas, security
import re

# ============================================================
# 1. Inicialização do roteador
# ============================================================

router = APIRouter()

def normalizar_placa(placa: str) -> str:
    """Remove hífens, espaços e converte para maiúscula."""
    if not placa:
        return ""
    # Remove tudo que não seja letra ou número
    placa_limpa = re.sub(r'[^A-Z0-9]', '', placa.upper())
    return placa_limpa

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

# ============================================================
# 2. Criar manutenção
# ============================================================

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def criar_manutencao(
    manutencao_data: schemas.ManutencaoCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova manutenção.
    - Verifica se o veículo existe e pertence ao usuário
    - Atualiza o KM do veículo automaticamente
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Normaliza a placa (remove hífens, espaços e converte para maiúscula)
    placa_normalizada = normalizar_placa(manutencao_data.placa)
    
    # Busca o veículo pela placa
    veiculo = db.execute(
        text("""
            SELECT id, km_atual, placa 
            FROM veiculos 
            WHERE REPLACE(REPLACE(UPPER(placa), '-', ''), ' ', '') = :placa 
            AND usuario_id = :usuario_id
        """),
        {"placa": placa_normalizada, "usuario_id": usuario_id}
    ).fetchone()
    
    if not veiculo:
        todos_veiculos = db.execute(
            text("SELECT placa FROM veiculos WHERE usuario_id = :usuario_id"),
            {"usuario_id": usuario_id}
        ).fetchall()
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veículo com placa '{manutencao_data.placa}' não encontrado. Placas disponíveis: {[v[0] for v in todos_veiculos]}"
        )
    
    veiculo_id = veiculo[0]
    km_atual_veiculo = veiculo[1]
    placa_original = veiculo[2]
    
    if manutencao_data.km < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A quilometragem não pode ser negativa"
        )
    
    try:
        # Insere usando os nomes corretos das colunas: data, km, descricao, prestador_servico
        db.execute(
            text("""
                INSERT INTO manutencoes 
                (veiculo_id, data, km, tipo_manutencao, prestador_servico, custo, descricao)
                VALUES (:veiculo_id, :data, :km, :tipo_manutencao, :prestador_servico, :custo, :descricao)
            """),
            {
                "veiculo_id": veiculo_id,
                "data": manutencao_data.data,
                "km": manutencao_data.km,
                "tipo_manutencao": manutencao_data.tipo_manutencao,
                "prestador_servico": manutencao_data.prestador,
                "custo": manutencao_data.custo,
                "descricao": manutencao_data.observacoes
            }
        )
        
        # Atualiza o KM do veículo
        if manutencao_data.km > km_atual_veiculo:
            db.execute(
                text("UPDATE veiculos SET km_atual = :km_atual WHERE id = :id"),
                {"km_atual": manutencao_data.km, "id": veiculo_id}
            )
        
        db.commit()
        
        return {
            "msg": "Manutenção cadastrada com sucesso",
            "placa": placa_original,
            "veiculo_id": veiculo_id,
            "km_veiculo_atualizado": manutencao_data.km > km_atual_veiculo
        }
        
    except Exception as e:
        db.rollback()
        print(f"ERRO ao criar manutenção: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cadastrar manutenção: {str(e)}"
        )


# ============================================================
# 3. Listar todas as manutenções
# ============================================================

@router.get("/", response_model=List[dict])
def listar_manutencoes(
    request: Request,
    db: Session = Depends(get_db),
    placa: Optional[str] = None
):
    """Lista todas as manutenções dos veículos do usuário logado."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    query = """
        SELECT m.id, v.placa, m.data, m.km, 
               m.tipo_manutencao, m.prestador_servico, m.custo, m.descricao
        FROM manutencoes m
        INNER JOIN veiculos v ON m.veiculo_id = v.id
        WHERE v.usuario_id = :usuario_id
    """
    params = {"usuario_id": usuario_id}
    
    if placa:
        placa_normalizada = normalizar_placa(placa)
        query += " AND REPLACE(REPLACE(UPPER(v.placa), '-', ''), ' ', '') LIKE :placa"
        params["placa"] = f"%{placa_normalizada}%"
    
    query += " ORDER BY m.data DESC"
    
    result = db.execute(text(query), params).fetchall()
    
    manutencoes = []
    for row in result:
        manutencoes.append({
            "id": row[0],
            "placa": row[1],
            "data": str(row[2]),
            "km": row[3],
            "tipo_manutencao": row[4],
            "prestador": row[5],
            "custo": float(row[6]),
            "observacoes": row[7]
        })
    
    return manutencoes


# ============================================================
# 4. Buscar manutenção por ID
# ============================================================

@router.get("/{manutencao_id}", response_model=dict)
def obter_manutencao(
    manutencao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém uma manutenção específica."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    result = db.execute(
        text("""
            SELECT m.id, v.placa, m.data, m.km,
                   m.tipo_manutencao, m.prestador_servico, m.custo, m.descricao, m.veiculo_id
            FROM manutencoes m
            INNER JOIN veiculos v ON m.veiculo_id = v.id
            WHERE m.id = :id AND v.usuario_id = :usuario_id
        """),
        {"id": manutencao_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manutenção não encontrada"
        )
    
    return {
        "id": result[0],
        "placa": result[1],
        "data": str(result[2]),
        "km": result[3],
        "tipo_manutencao": result[4],
        "prestador": result[5],
        "custo": float(result[6]),
        "observacoes": result[7],
        "veiculo_id": result[8]
    }


# ============================================================
# 5. Atualizar manutenção
# ============================================================

@router.put("/{manutencao_id}", response_model=dict)
def atualizar_manutencao(
    manutencao_id: int,
    manutencao_data: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza uma manutenção existente."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    existing = db.execute(
        text("""
            SELECT m.id, m.veiculo_id, v.placa
            FROM manutencoes m
            INNER JOIN veiculos v ON m.veiculo_id = v.id
            WHERE m.id = :id AND v.usuario_id = :usuario_id
        """),
        {"id": manutencao_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manutenção não encontrada"
        )
    
    veiculo_id_atual = existing[1]
    
    nova_placa = manutencao_data.get("placa")
    if nova_placa:
        placa_normalizada = normalizar_placa(nova_placa)
        
        veiculo = db.execute(
            text("""
                SELECT id 
                FROM veiculos 
                WHERE REPLACE(REPLACE(UPPER(placa), '-', ''), ' ', '') = :placa 
                AND usuario_id = :usuario_id
            """),
            {"placa": placa_normalizada, "usuario_id": usuario_id}
        ).fetchone()
        
        if not veiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Veículo com placa '{nova_placa}' não encontrado"
            )
        
        veiculo_id = veiculo[0]
    else:
        veiculo_id = veiculo_id_atual
    
    try:
        db.execute(
            text("""
                UPDATE manutencoes 
                SET veiculo_id = :veiculo_id,
                    data = :data,
                    km = :km,
                    tipo_manutencao = :tipo_manutencao,
                    prestador_servico = :prestador_servico,
                    custo = :custo,
                    descricao = :descricao
                WHERE id = :id
            """),
            {
                "id": manutencao_id,
                "veiculo_id": veiculo_id,
                "data": manutencao_data.get("data"),
                "km": manutencao_data.get("km"),
                "tipo_manutencao": manutencao_data.get("tipo_manutencao"),
                "prestador_servico": manutencao_data.get("prestador"),
                "custo": manutencao_data.get("custo"),
                "descricao": manutencao_data.get("observacoes", "")
            }
        )
        db.commit()
        
        return {"msg": "Manutenção atualizada com sucesso"}
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao atualizar manutenção: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar manutenção"
        )


# ============================================================
# 6. Excluir manutenção
# ============================================================

@router.delete("/{manutencao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_manutencao(
    manutencao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Deleta uma manutenção."""
    usuario_id = get_usuario_id_from_token(request, db)
    
    existing = db.execute(
        text("""
            SELECT m.id
            FROM manutencoes m
            INNER JOIN veiculos v ON m.veiculo_id = v.id
            WHERE m.id = :id AND v.usuario_id = :usuario_id
        """),
        {"id": manutencao_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manutenção não encontrada"
        )
    
    try:
        db.execute(
            text("DELETE FROM manutencoes WHERE id = :id"),
            {"id": manutencao_id}
        )
        db.commit()
        return None
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao deletar manutenção: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar manutenção"
        )
