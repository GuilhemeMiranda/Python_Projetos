from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db

# ============================================================
# 1. Inicialização do roteador
# ============================================================

router = APIRouter(
    prefix="/veiculos",      # URL base do módulo
    tags=["Veículos"]        # Agrupa visualmente no Swagger
)

# ============================================================
# 2. Endpoint: Criar novo veículo
# ============================================================

@router.post("/", response_model=schemas.VeiculoResponse, status_code=status.HTTP_201_CREATED)
def criar_veiculo(veiculo: schemas.VeiculoCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo veículo no sistema.
    - Requer JSON com: placa, modelo, marca, ano, km_atual, usuario_id.
    """
    novo_veiculo = crud.criar_veiculo(db, veiculo)
    return novo_veiculo


# ============================================================
# 3. Endpoint: Listar veículos
# ============================================================

@router.get("/", response_model=List[schemas.VeiculoResponse])
def listar_veiculos(db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os veículos cadastrados.
    """
    return crud.listar_veiculos(db)


# ============================================================
# 4. Endpoint: Buscar veículo por ID
# ============================================================

@router.get("/{veiculo_id}", response_model=schemas.VeiculoResponse)
def buscar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """
    Busca um veículo específico pelo ID.
    """
    veiculo = crud.buscar_veiculo_por_id(db, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    return veiculo


# ============================================================
# 5. Endpoint: Atualizar veículo
# ============================================================

@router.put("/{veiculo_id}", response_model=schemas.VeiculoResponse)
def atualizar_veiculo(veiculo_id: int, dados: schemas.VeiculoBase, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um veículo existente.
    - Exemplo: alterar km_atual, modelo, marca.
    """
    veiculo_atualizado = crud.atualizar_veiculo(db, veiculo_id, dados)
    if not veiculo_atualizado:
        raise HTTPException(status_code=404, detail="Veículo não encontrado para atualização.")
    return veiculo_atualizado


# ============================================================
# 6. Endpoint: Excluir veículo
# ============================================================

@router.delete("/{veiculo_id}", response_model=schemas.VeiculoResponse)
def excluir_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """
    Exclui um veículo do banco de dados.
    """
    veiculo = crud.excluir_veiculo(db, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado para exclusão.")
    return veiculo
