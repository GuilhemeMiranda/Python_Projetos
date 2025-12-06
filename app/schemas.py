from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime

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
# Schemas de Plano de Manutenção (NOVA ESTRUTURA)
# ============================================================

class PlanoManutencaoBase(BaseModel):
    """Schema base para Plano de Manutenção"""
    nome: str = Field(..., min_length=3, max_length=200, description="Nome do plano")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do plano")
    km_intervalo: Optional[int] = Field(None, gt=0, description="Intervalo em KM (deve ser maior que 0)")
    dias_intervalo: Optional[int] = Field(None, gt=0, description="Intervalo em dias (deve ser maior que 0)")
    
    @validator('km_intervalo', 'dias_intervalo')
    def validar_pelo_menos_um_intervalo(cls, v, values):
        """Garante que pelo menos um intervalo foi definido"""
        if 'km_intervalo' in values:
            if values.get('km_intervalo') is None and v is None:
                raise ValueError('Deve informar pelo menos um intervalo (KM ou dias)')
        return v


class PlanoManutencaoCreate(PlanoManutencaoBase):
    """Schema para criar um novo Plano"""
    pass


class PlanoManutencaoUpdate(BaseModel):
    """Schema para atualizar um Plano (todos os campos opcionais)"""
    nome: Optional[str] = Field(None, min_length=3, max_length=200)
    descricao: Optional[str] = None
    km_intervalo: Optional[int] = Field(None, gt=0)
    dias_intervalo: Optional[int] = Field(None, gt=0)


class PlanoManutencaoResponse(PlanoManutencaoBase):
    """Schema de resposta com dados completos do Plano"""
    id: int
    usuario_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# Schemas de Vínculo Veículo-Plano
# ============================================================

class VeiculoPlanoBase(BaseModel):
    """Schema base para vínculo Veículo-Plano"""
    data_inicio: date = Field(..., description="Data de início do plano")
    proxima_manutencao_km: Optional[int] = Field(None, ge=0, description="KM da próxima manutenção")
    proxima_manutencao_data: Optional[date] = Field(None, description="Data da próxima manutenção")
    ativo: bool = Field(True, description="Se o plano está ativo")


class VeiculoPlanoCreate(VeiculoPlanoBase):
    """Schema para vincular um veículo a um plano"""
    veiculo_id: int = Field(..., gt=0, description="ID do veículo")
    plano_manutencao_id: int = Field(..., gt=0, description="ID do plano")


class VeiculoPlanoUpdate(BaseModel):
    """Schema para atualizar vínculo (todos opcionais)"""
    data_inicio: Optional[date] = None
    proxima_manutencao_km: Optional[int] = Field(None, ge=0)
    proxima_manutencao_data: Optional[date] = None
    ativo: Optional[bool] = None


class VeiculoPlanoResponse(VeiculoPlanoBase):
    """Schema de resposta com dados completos do vínculo"""
    id: int
    veiculo_id: int
    plano_manutencao_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# Schemas com Relacionamentos
# ============================================================

class PlanoComVeiculos(PlanoManutencaoResponse):
    """Plano com lista de veículos vinculados"""
    veiculos: List[VeiculoPlanoResponse] = []


class VeiculoPlanoComDetalhes(VeiculoPlanoResponse):
    """Vínculo com detalhes do plano"""
    plano: Optional[PlanoManutencaoResponse] = None
