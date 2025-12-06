from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text, Boolean, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# -----------------------------------------------------------
# 1. Tabela de Usuários
# -----------------------------------------------------------
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)

    # Relacionamento 1:N → Usuário tem vários veículos
    veiculos = relationship("Veiculo", back_populates="usuario")
    # Relacionamento 1:N → Usuário tem vários planos
    planos = relationship("PlanoManutencao", back_populates="usuario", cascade="all, delete-orphan")

# -----------------------------------------------------------
# 2. Tabela de Veículos
# -----------------------------------------------------------
class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(10), unique=True, nullable=False)
    modelo = Column(String(100), nullable=False)
    marca = Column(String(100))
    ano = Column(Integer)
    km_atual = Column(Integer)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="veiculos")
    manutencoes = relationship("Manutencao", back_populates="veiculo")
    # Relacionamento N:N com planos através de VeiculoPlano
    vinculos_planos = relationship("VeiculoPlano", back_populates="veiculo", cascade="all, delete-orphan")

# -----------------------------------------------------------
# 3. Tabela de Manutenções
# -----------------------------------------------------------
class Manutencao(Base):
    __tablename__ = "manutencoes"

    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    data = Column(Date)
    km = Column(Integer)
    tipo_manutencao = Column(String(100))
    descricao = Column(Text)
    custo = Column(Float)
    prestador_servico = Column(String(150))

    # Relacionamentos
    veiculo = relationship("Veiculo", back_populates="manutencoes")
    documentos = relationship("Documento", back_populates="manutencao")

# -----------------------------------------------------------
# 4. Tabela de Documentos
# -----------------------------------------------------------
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    manutencao_id = Column(Integer, ForeignKey("manutencoes.id"), nullable=False)
    nome_arquivo = Column(String(200), nullable=False)
    tipo = Column(String(50))
    caminho_arquivo = Column(String(250))

    # Relacionamento com manutenção
    manutencao = relationship("Manutencao", back_populates="documentos")

# -----------------------------------------------------------
# 5. Tabela de Planos de Manutenção (NOVA ESTRUTURA)
# -----------------------------------------------------------
class PlanoManutencao(Base):
    """
    Planos de manutenção preventiva vinculados ao usuário.
    Permite definir intervalos por KM e/ou dias.
    Relacionamento N:N com veículos através de VeiculoPlano.
    """
    __tablename__ = "planos_manutencao"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)
    km_intervalo = Column(Integer, nullable=True)
    dias_intervalo = Column(Integer, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="planos")
    veiculos = relationship("VeiculoPlano", back_populates="plano", cascade="all, delete-orphan")
    
    # Constraints: Pelo menos um intervalo deve ser informado
    __table_args__ = (
        CheckConstraint('km_intervalo IS NULL OR km_intervalo > 0', name='chk_km_positivo'),
        CheckConstraint('dias_intervalo IS NULL OR dias_intervalo > 0', name='chk_dias_positivo'),
        CheckConstraint('km_intervalo IS NOT NULL OR dias_intervalo IS NOT NULL', name='chk_um_intervalo'),
    )
    
    def __repr__(self):
        return f"<PlanoManutencao(id={self.id}, nome='{self.nome}')>"

# -----------------------------------------------------------
# 6. Tabela de Vínculo Veículo-Plano (N:N)
# -----------------------------------------------------------
class VeiculoPlano(Base):
    """
    Tabela associativa para relacionamento N:N entre veículos e planos.
    - Um veículo pode ter múltiplos planos de manutenção.
    - Um plano pode ser aplicado a múltiplos veículos.
    """
    __tablename__ = "veiculos_planos"
    
    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id", ondelete="CASCADE"), nullable=False)
    plano_manutencao_id = Column(Integer, ForeignKey("planos_manutencao.id", ondelete="CASCADE"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    proxima_manutencao_km = Column(Integer, nullable=True)
    proxima_manutencao_data = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    veiculo = relationship("Veiculo", back_populates="vinculos_planos")
    plano = relationship("PlanoManutencao", back_populates="veiculos")
    
    # Constraint: Um veículo não pode ter o mesmo plano duplicado
    __table_args__ = (
        UniqueConstraint('veiculo_id', 'plano_manutencao_id', name='uk_veiculo_plano'),
    )
    
    def __repr__(self):
        return f"<VeiculoPlano(veiculo_id={self.veiculo_id}, plano_id={self.plano_manutencao_id})>"
