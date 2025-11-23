from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import date

# ============================================================
# 1. Schemas de USUÁRIO
# ============================================================

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str  # senha em texto puro, será convertida para hash depois

class UsuarioResponse(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 2. Schemas de VEÍCULO
# ============================================================

class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    marca: Optional[str] = None
    ano: Optional[int] = None
    km_atual: Optional[int] = 0

class VeiculoCreate(VeiculoBase):
    usuario_id: int

class VeiculoResponse(VeiculoBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 3. Schemas de MANUTENÇÃO
# ============================================================

class ManutencaoBase(BaseModel):
    veiculo_id: int
    data: Optional[date] = None
    km: Optional[int] = None
    tipo_manutencao: Optional[str] = None
    descricao: Optional[str] = None
    custo: Optional[float] = None
    prestador_servico: Optional[str] = None

class ManutencaoCreate(ManutencaoBase):
    pass  # por enquanto, sem campos extras

class ManutencaoResponse(ManutencaoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 4. Schemas de DOCUMENTOS
# ============================================================

class DocumentoBase(BaseModel):
    manutencao_id: int
    nome_arquivo: str
    tipo: Optional[str] = None
    caminho_arquivo: Optional[str] = None

class DocumentoCreate(DocumentoBase):
    pass

class DocumentoResponse(DocumentoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 5. Schemas de PLANOS DE MANUTENÇÃO
# ============================================================

class PlanoManutencaoBase(BaseModel):
    veiculo_id: int
    nome_plano: str
    km_referencia: Optional[int] = None
    servicos: Optional[str] = None

class PlanoManutencaoCreate(PlanoManutencaoBase):
    pass

class PlanoManutencaoResponse(PlanoManutencaoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
