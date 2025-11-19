from pydantic import BaseModel
from typing import Optional
from datetime import date

# ===== SCHEMAS DE USUÁRIO =====
class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# Alias para compatibilidade
UsuarioResponse = Usuario

# ===== SCHEMAS DE VEÍCULO =====
class VeiculoBase(BaseModel):
    placa: str
    ano: int
    marca: str
    modelo: str
    km_atual: int

class VeiculoCreate(VeiculoBase):
    pass

class Veiculo(VeiculoBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

# Alias para compatibilidade
VeiculoResponse = Veiculo

# ===== SCHEMAS DE MANUTENÇÃO =====
class ManutencaoBase(BaseModel):
    veiculo_id: int
    data: date
    km: int
    tipo: str
    prestador: Optional[str] = None
    custo: Optional[float] = None

class ManutencaoCreate(ManutencaoBase):
    pass

class Manutencao(ManutencaoBase):
    id: int

    class Config:
        from_attributes = True

# Alias para compatibilidade
ManutencaoResponse = Manutencao

# ===== SCHEMAS DE PLANO DE MANUTENÇÃO =====
class PlanoBase(BaseModel):
    veiculo_id: int
    tipo_manutencao: str
    km_previsto: int
    data_prevista: Optional[date] = None

class PlanoCreate(PlanoBase):
    pass

class Plano(PlanoBase):
    id: int

    class Config:
        from_attributes = True

# Alias para compatibilidade
PlanoResponse = Plano
PlanoManutencaoCreate = PlanoCreate
PlanoManutencaoResponse = Plano
