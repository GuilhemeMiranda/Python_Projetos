#Módulo: routes/planos.py
#Define as rotas de gerenciamento dos planos de manutenção preventiva.


from fastapi import APIRouter, HTTPException, status
from typing import List

# ============================================================
# Inicialização do roteador
# ============================================================

router = APIRouter()  # SEM prefix aqui

# ============================================================
# Rotas de Planos de Manutenção
# ============================================================

@router.get("/", response_model=List[dict])
def listar_planos():
    """Lista todos os planos de manutenção (funcionalidade futura)."""
    return []

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_plano(plano: dict):
    """Cria um novo plano de manutenção (funcionalidade futura)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidade em desenvolvimento"
    )

@router.get("/{plano_id}")
def obter_plano(plano_id: int):
    """Obtém um plano de manutenção (funcionalidade futura)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidade em desenvolvimento"
    )

@router.put("/{plano_id}")
def atualizar_plano(plano_id: int, plano: dict):
    """Atualiza um plano de manutenção (funcionalidade futura)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidade em desenvolvimento"
    )

@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_plano(plano_id: int):
    """Deleta um plano de manutenção (funcionalidade futura)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidade em desenvolvimento"
    )
