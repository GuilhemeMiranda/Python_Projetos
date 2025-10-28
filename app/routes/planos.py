#Módulo: routes/planos.py
#Define as rotas de gerenciamento dos planos de manutenção preventiva.


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

# ============================================================
# 1. Inicialização do roteador
# ============================================================

router = APIRouter(
    prefix="/planos",
    tags=["Planos de Manutenção"]
)

# ============================================================
# 2. Criar um plano de manutenção
# ============================================================

@router.post("/", response_model=schemas.PlanoManutencaoResponse, status_code=status.HTTP_201_CREATED)
def criar_plano(plano: schemas.PlanoManutencaoCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo plano de manutenção preventiva.
    - Requer: veiculo_id, nome_plano, km_referencia, servicos.
    """
    veiculo = crud.buscar_veiculo_por_id(db, plano.veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    novo_plano = crud.criar_plano(db, plano)
    return novo_plano


# ============================================================
# 3. Listar todos os planos
# ============================================================

@router.get("/", response_model=List[schemas.PlanoManutencaoResponse])
def listar_planos(db: Session = Depends(get_db)):
    """
    Retorna todos os planos de manutenção cadastrados.
    """
    return crud.listar_planos(db)


# ============================================================
# 4. Buscar planos de um veículo específico
# ============================================================

@router.get("/veiculo/{veiculo_id}", response_model=List[schemas.PlanoManutencaoResponse])
def listar_planos_por_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """
    Lista todos os planos de manutenção vinculados a um veículo.
    """
    veiculo = crud.buscar_veiculo_por_id(db, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    planos = db.query(crud.models.PlanoManutencao).filter(crud.models.PlanoManutencao.veiculo_id == veiculo_id).all()
    return planos


# ============================================================
# 5. Excluir um plano de manutenção
# ============================================================

@router.delete("/{plano_id}", response_model=schemas.PlanoManutencaoResponse)
def excluir_plano(plano_id: int, db: Session = Depends(get_db)):
    """
    Exclui um plano de manutenção pelo ID.
    """
    plano = crud.excluir_plano(db, plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano de manutenção não encontrado.")
    return plano
