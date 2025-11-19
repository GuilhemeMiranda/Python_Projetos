#Módulo: routes/manutencoes.py
#Define as rotas para cadastro, listagem e gerenciamento de manutenções.

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app import crud, schemas, security
from app.database import get_db

# ============================================================
# 1. Inicialização do roteador
# ============================================================

router = APIRouter(
    prefix="/manutencoes",
    tags=["Manutenções"]
)

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

# ============================================================
# 2. Criar manutenção
# ============================================================

@router.post("/", response_model=schemas.Manutencao, status_code=status.HTTP_201_CREATED)
def criar_manutencao(
    manutencao_data: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova manutenção. Aceita placa do veículo ao invés do ID.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    placa = manutencao_data.get("placa")
    if not placa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Placa do veículo obrigatória"
        )
    
    # Busca o veículo pela placa e verifica se pertence ao usuário
    veiculo = db.query(models.Veiculo).filter(
        models.Veiculo.placa == placa,
        models.Veiculo.usuario_id == usuario_id
    ).first()
    
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado ou não pertence ao usuário"
        )
    
    # Cria a manutenção
    nova_manutencao = models.Manutencao(
        veiculo_id=veiculo.id,
        data=manutencao_data.get("data"),
        km=manutencao_data.get("km"),
        tipo=manutencao_data.get("tipo"),
        prestador=manutencao_data.get("prestador"),
        custo=manutencao_data.get("custo"),
    )
    
    db.add(nova_manutencao)
    db.commit()
    db.refresh(nova_manutencao)
    
    return nova_manutencao


# ============================================================
# 3. Listar todas as manutenções
# ============================================================

@router.get("/", response_model=List[dict])
def listar_manutencoes(
    request: Request,
    db: Session = Depends(get_db),
    placa: str = None
):
    """
    Lista todas as manutenções dos veículos do usuário logado.
    Opcionalmente filtra por placa.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Busca manutenções com join para obter dados do veículo
    query = """
        SELECT 
            m.id,
            v.placa,
            m.data,
            m.km,
            m.tipo,
            m.prestador,
            m.custo
        FROM manutencoes m
        INNER JOIN veiculos v ON m.veiculo_id = v.id
        WHERE v.usuario_id = :usuario_id
    """
    
    params = {"usuario_id": usuario_id}
    
    if placa:
        query += " AND v.placa LIKE :placa"
        params["placa"] = f"%{placa}%"
    
    query += " ORDER BY m.data DESC"
    
    result = db.execute(text(query), params).fetchall()
    
    # Converte para lista de dicts
    manutencoes = []
    for row in result:
        manutencoes.append({
            "id": row[0],
            "placa": row[1],
            "data": str(row[2]),
            "km": row[3],
            "tipo": row[4],
            "prestador": row[5],
            "custo": row[6]
        })
    
    return manutencoes


# ============================================================
# 4. Buscar manutenção por ID
# ============================================================

@router.get("/{manutencao_id}", response_model=schemas.Manutencao)
def obter_manutencao(
    manutencao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Obtém uma manutenção específica.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Verifica se a manutenção pertence a um veículo do usuário
    manutencao = db.execute(
        text("""
            SELECT m.* FROM manutencoes m
            INNER JOIN veiculos v ON m.veiculo_id = v.id
            WHERE m.id = :manutencao_id AND v.usuario_id = :usuario_id
        """),
        {"manutencao_id": manutencao_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not manutencao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manutenção não encontrada"
        )
    
    return manutencao


# ============================================================
# 5. Excluir manutenção
# ============================================================

@router.delete("/{manutencao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_manutencao(
    manutencao_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Deleta uma manutenção.
    """
    usuario_id = get_usuario_id_from_token(request, db)
    
    # Busca a manutenção e verifica se pertence ao usuário
    manutencao = db.execute(
        text("""
            SELECT m.* FROM manutencoes m
            INNER JOIN veiculos v ON m.veiculo_id = v.id
            WHERE m.id = :manutencao_id AND v.usuario_id = :usuario_id
        """),
        {"manutencao_id": manutencao_id, "usuario_id": usuario_id}
    ).fetchone()
    
    if not manutencao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manutenção não encontrada"
        )
    
    db.execute(
        text("DELETE FROM manutencoes WHERE id = :manutencao_id"),
        {"manutencao_id": manutencao_id}
    )
    db.commit()
    
    return None
