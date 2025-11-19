from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# ============================================================
# Schemas de Usuário
# ============================================================

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# ============================================================
# Schemas de Veículo
# ============================================================

class VeiculoBase(BaseModel):
    placa: str
    ano: int
    marca: str
    modelo: str
    km_atual: int

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoResponse(VeiculoBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

# ============================================================
# Schemas de Manutenção
# ============================================================

class ManutencaoBase(BaseModel):
    placa: str
    data: date
    km: int
    tipo_manutencao: str
    prestador: str  # Será mapeado para prestador_servico
    custo: float
    observacoes: Optional[str] = None  # Será mapeado para descricao

class ManutencaoCreate(ManutencaoBase):
    """Schema para criação de manutenção usando a placa do veículo"""
    pass

class ManutencaoUpdate(BaseModel):
    """Schema para atualização de manutenção"""
    placa: Optional[str] = None
    data: Optional[date] = None
    km: Optional[int] = None
    tipo_manutencao: Optional[str] = None
    prestador: Optional[str] = None
    custo: Optional[float] = None
    observacoes: Optional[str] = None

class ManutencaoResponse(BaseModel):
    id: int
    veiculo_id: int
    data: date
    km: int
    tipo_manutencao: str
    prestador: str
    custo: float
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================
# Schemas de Plano de Manutenção
# ============================================================

class PlanoManutencaoBase(BaseModel):
    veiculo_id: int
    nome_plano: str
    km_referencia: int
    servicos: Optional[str] = None

class PlanoManutencaoCreate(PlanoManutencaoBase):
    pass

class PlanoManutencaoUpdate(BaseModel):
    nome_plano: Optional[str] = None
    km_referencia: Optional[int] = None
    servicos: Optional[str] = None

class PlanoManutencaoResponse(PlanoManutencaoBase):
    id: int

    class Config:
        from_attributes = True
