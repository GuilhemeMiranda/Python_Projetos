from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
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
    planos = relationship("PlanoManutencao", back_populates="veiculo")

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
# 5. Tabela de Planos de Manutenção
# -----------------------------------------------------------
class PlanoManutencao(Base):
    __tablename__ = "planos_manutencao"

    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    nome_plano = Column(String(100))
    km_referencia = Column(Integer)
    servicos = Column(Text)

    # Relacionamento com veículo
    veiculo = relationship("Veiculo", back_populates="planos")
