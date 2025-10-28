#Módulo: routes/manutencoes.py
#Define as rotas para cadastro, listagem e gerenciamento de manutenções.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

# ============================================================
# 1. Inicialização do roteador
# ============================================================

router = APIRouter(
    prefix="/manutencoes",
    tags=["Manutenções"]
)

# ============================================================
# 2. Criar manutenção
# ============================================================

@router.post("/", response_model=schemas.ManutencaoResponse, status_code=status.HTTP_201_CREATED)
def criar_manutencao(manutencao: schemas.ManutencaoCreate, db: Session = Depends(get_db)):
    """
    Cadastra uma nova manutenção.
    - Requer: veiculo_id, data, km, tipo_manutencao, descricao, custo, prestador_servico.
    """
    # Verifica se o veículo existe
    veiculo = crud.buscar_veiculo_por_id(db, manutencao.veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    nova_manutencao = crud.criar_manutencao(db, manutencao)
    return nova_manutencao


# ============================================================
# 3. Listar todas as manutenções
# ============================================================

@router.get("/", response_model=List[schemas.ManutencaoResponse])
def listar_manutencoes(db: Session = Depends(get_db)):
    """
    Retorna a lista de todas as manutenções cadastradas.
    """
    return crud.listar_manutencoes(db)


# ============================================================
# 4. Buscar manutenção por ID
# ============================================================

@router.get("/{manutencao_id}", response_model=schemas.ManutencaoResponse)
def buscar_manutencao(manutencao_id: int, db: Session = Depends(get_db)):
    """
    Busca uma manutenção específica pelo ID.
    """
    manutencao = crud.buscar_manutencao_por_id(db, manutencao_id)
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada.")
    return manutencao


# ============================================================
# 5. Excluir manutenção
# ============================================================

@router.delete("/{manutencao_id}", response_model=schemas.ManutencaoResponse)
def excluir_manutencao(manutencao_id: int, db: Session = Depends(get_db)):
    """
    Remove uma manutenção do banco de dados.
    """
    manutencao = crud.excluir_manutencao(db, manutencao_id)
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada para exclusão.")
    return manutencao
