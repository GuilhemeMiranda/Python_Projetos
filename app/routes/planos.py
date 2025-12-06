"""
Módulo: routes/planos.py
Define as rotas de gerenciamento dos planos de manutenção preventiva.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import crud, schemas
from app.database import get_db

# ============================================================
# Inicialização do roteador
# ============================================================

router = APIRouter()

# ============================================================
# Rotas de Planos de Manutenção
# ============================================================

@router.post("/", response_model=schemas.PlanoManutencaoResponse, status_code=status.HTTP_201_CREATED)
def criar_plano(
    plano: schemas.PlanoManutencaoCreate,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Cria um novo plano de manutenção para o usuário.
    
    - **nome**: Nome do plano (ex: "Troca de Óleo")
    - **descricao**: Descrição detalhada (opcional)
    - **km_intervalo**: Intervalo em KM (opcional, mas pelo menos um intervalo é obrigatório)
    - **dias_intervalo**: Intervalo em dias (opcional, mas pelo menos um intervalo é obrigatório)
    """
    try:
        db_plano = crud.create_plano(db=db, plano=plano, usuario_id=usuario_id)
        return db_plano
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar plano: {str(e)}"
        )


@router.get("/", response_model=List[schemas.PlanoManutencaoResponse])
def listar_planos(
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os planos de manutenção do usuário.
    
    - **usuario_id**: ID do usuário
    - **skip**: Número de registros para pular (paginação)
    - **limit**: Número máximo de registros
    """
    planos = crud.get_planos(db=db, usuario_id=usuario_id, skip=skip, limit=limit)
    return planos


@router.get("/{plano_id}", response_model=schemas.PlanoManutencaoResponse)
def obter_plano(plano_id: int, db: Session = Depends(get_db)):
    """
    Obtém um plano de manutenção específico por ID.
    """
    db_plano = crud.get_plano(db=db, plano_id=plano_id)
    if db_plano is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plano {plano_id} não encontrado"
        )
    return db_plano


@router.put("/{plano_id}", response_model=schemas.PlanoManutencaoResponse)
def atualizar_plano(
    plano_id: int,
    plano: schemas.PlanoManutencaoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um plano de manutenção existente.
    Apenas os campos fornecidos serão atualizados.
    """
    db_plano = crud.update_plano(db=db, plano_id=plano_id, plano=plano)
    if db_plano is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plano {plano_id} não encontrado"
        )
    return db_plano


@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_plano(plano_id: int, db: Session = Depends(get_db)):
    """
    Deleta um plano de manutenção.
    Também remove automaticamente todos os vínculos com veículos (CASCADE).
    """
    sucesso = crud.delete_plano(db=db, plano_id=plano_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plano {plano_id} não encontrado"
        )
    return None


# ============================================================
# Rotas de Vínculo Veículo-Plano
# ============================================================

@router.post("/vincular", response_model=schemas.VeiculoPlanoResponse, status_code=status.HTTP_201_CREATED)
def vincular_veiculo_ao_plano(
    veiculo_id: int,
    plano_id: int,
    data_inicio: date,
    db: Session = Depends(get_db)
):
    """
    Vincula um veículo a um plano de manutenção.
    
    - **veiculo_id**: ID do veículo
    - **plano_id**: ID do plano
    - **data_inicio**: Data de início do plano no veículo
    """
    try:
        db_vinculo = crud.vincular_veiculo_plano(
            db=db,
            veiculo_id=veiculo_id,
            plano_id=plano_id,
            data_inicio=data_inicio
        )
        return db_vinculo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao vincular: {str(e)}"
        )


@router.delete("/vincular", status_code=status.HTTP_204_NO_CONTENT)
def desvincular_veiculo_do_plano(
    veiculo_id: int,
    plano_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove o vínculo entre um veículo e um plano.
    """
    sucesso = crud.desvincular_veiculo_plano(db=db, veiculo_id=veiculo_id, plano_id=plano_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vínculo não encontrado"
        )
    return None


@router.get("/veiculo/{veiculo_id}/planos", response_model=List[schemas.VeiculoPlanoResponse])
def listar_planos_do_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """
    Lista todos os planos vinculados a um veículo.
    """
    vinculos = crud.get_planos_do_veiculo(db=db, veiculo_id=veiculo_id)
    return vinculos


@router.get("/plano/{plano_id}/veiculos", response_model=List[schemas.VeiculoPlanoResponse])
def listar_veiculos_do_plano(plano_id: int, db: Session = Depends(get_db)):
    """
    Lista todos os veículos vinculados a um plano.
    """
    vinculos = crud.get_veiculos_do_plano(db=db, plano_id=plano_id)
    return vinculos


@router.put("/vincular/{veiculo_plano_id}", response_model=schemas.VeiculoPlanoResponse)
def atualizar_vinculo(
    veiculo_plano_id: int,
    vinculo: schemas.VeiculoPlanoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um vínculo existente entre veículo e plano.
    Útil para atualizar próximas manutenções ou desativar o plano.
    """
    db_vinculo = crud.update_veiculo_plano(db=db, veiculo_plano_id=veiculo_plano_id, vinculo=vinculo)
    if db_vinculo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vínculo {veiculo_plano_id} não encontrado"
        )
    return db_vinculo
