from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models, schemas
from typing import List, Optional
from datetime import date
import hashlib

# ============================================================
# CRUD de Usuários
# ============================================================

def get_usuario(db: Session, usuario_id: int):
    """Busca um usuário por ID."""
    result = db.execute(
        text("SELECT * FROM usuarios WHERE id = :id"),
        {"id": usuario_id}
    ).fetchone()
    return result

def get_usuario_by_email(db: Session, email: str):
    """Busca um usuário por e-mail."""
    result = db.execute(
        text("SELECT * FROM usuarios WHERE email = :email"),
        {"email": email}
    ).fetchone()
    return result

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos os usuários."""
    result = db.execute(
        text("SELECT * FROM usuarios LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).fetchall()
    return result

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Cria um novo usuário."""
    hashed_password = hashlib.sha256(usuario.senha.encode()).hexdigest()
    
    db.execute(
        text("""
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (:nome, :email, :senha_hash)
        """),
        {
            "nome": usuario.nome,
            "email": usuario.email,
            "senha_hash": hashed_password
        }
    )
    db.commit()
    
    return get_usuario_by_email(db, email=usuario.email)

# ============================================================
# CRUD de Veículos
# ============================================================

def get_veiculo(db: Session, veiculo_id: int):
    """Busca um veículo por ID."""
    result = db.execute(
        text("SELECT * FROM veiculos WHERE id = :id"),
        {"id": veiculo_id}
    ).fetchone()
    return result

def get_veiculos_by_usuario(db: Session, usuario_id: int):
    """Lista todos os veículos de um usuário."""
    result = db.execute(
        text("SELECT * FROM veiculos WHERE usuario_id = :usuario_id"),
        {"usuario_id": usuario_id}
    ).fetchall()
    return result

def create_veiculo(db: Session, veiculo: schemas.VeiculoCreate, usuario_id: int):
    """Cria um novo veículo."""
    db.execute(
        text("""
            INSERT INTO veiculos (placa, ano, marca, modelo, km_atual, usuario_id)
            VALUES (:placa, :ano, :marca, :modelo, :km_atual, :usuario_id)
        """),
        {
            "placa": veiculo.placa,
            "ano": veiculo.ano,
            "marca": veiculo.marca,
            "modelo": veiculo.modelo,
            "km_atual": veiculo.km_atual,
            "usuario_id": usuario_id
        }
    )
    db.commit()
    
    result = db.execute(
        text("SELECT * FROM veiculos WHERE placa = :placa AND usuario_id = :usuario_id"),
        {"placa": veiculo.placa, "usuario_id": usuario_id}
    ).fetchone()
    return result

# ============================================================
# CRUD de Manutenções
# ============================================================

def get_manutencao(db: Session, manutencao_id: int):
    """Busca uma manutenção por ID."""
    result = db.execute(
        text("SELECT * FROM manutencoes WHERE id = :id"),
        {"id": manutencao_id}
    ).fetchone()
    return result

def get_manutencoes_by_veiculo(db: Session, veiculo_id: int):
    """Lista todas as manutenções de um veículo."""
    result = db.execute(
        text("SELECT * FROM manutencoes WHERE veiculo_id = :veiculo_id ORDER BY data_manutencao DESC"),
        {"veiculo_id": veiculo_id}
    ).fetchall()
    return result

def create_manutencao(db: Session, manutencao: schemas.ManutencaoCreate, veiculo_id: int):
    """Cria uma nova manutenção."""
    db.execute(
        text("""
            INSERT INTO manutencoes 
            (veiculo_id, data_manutencao, km_manutencao, tipo_manutencao, prestador, custo, observacoes)
            VALUES (:veiculo_id, :data_manutencao, :km_manutencao, :tipo_manutencao, :prestador, :custo, :observacoes)
        """),
        {
            "veiculo_id": veiculo_id,
            "data_manutencao": manutencao.data_manutencao,
            "km_manutencao": manutencao.km_manutencao,
            "tipo_manutencao": manutencao.tipo_manutencao,
            "prestador": manutencao.prestador,
            "custo": manutencao.custo,
            "observacoes": manutencao.observacoes
        }
    )
    db.commit()
    
    result = db.execute(
        text("SELECT * FROM manutencoes WHERE veiculo_id = :veiculo_id ORDER BY id DESC LIMIT 1"),
        {"veiculo_id": veiculo_id}
    ).fetchone()
    return result

# ============================================================
# CRUD de Planos de Manutenção (NOVA ESTRUTURA)
# ============================================================

def get_plano(db: Session, plano_id: int):
    """Busca um plano por ID."""
    return db.query(models.PlanoManutencao).filter(models.PlanoManutencao.id == plano_id).first()


def get_planos(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    """Lista todos os planos de um usuário."""
    return db.query(models.PlanoManutencao)\
        .filter(models.PlanoManutencao.usuario_id == usuario_id)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_plano(db: Session, plano: schemas.PlanoManutencaoCreate, usuario_id: int):
    """Cria um novo plano."""
    db_plano = models.PlanoManutencao(
        nome=plano.nome,
        descricao=plano.descricao,
        km_intervalo=plano.km_intervalo,
        dias_intervalo=plano.dias_intervalo,
        usuario_id=usuario_id
    )
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano


def update_plano(db: Session, plano_id: int, plano: schemas.PlanoManutencaoUpdate):
    """Atualiza um plano existente."""
    db_plano = get_plano(db, plano_id)
    if not db_plano:
        return None
    
    update_data = plano.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plano, key, value)
    
    db.commit()
    db.refresh(db_plano)
    return db_plano


def delete_plano(db: Session, plano_id: int):
    """Deleta um plano."""
    db_plano = get_plano(db, plano_id)
    if not db_plano:
        return False
    
    db.delete(db_plano)
    db.commit()
    return True


# ============================================================
# CRUD de Vínculo Veículo-Plano
# ============================================================

def get_veiculo_plano(db: Session, veiculo_plano_id: int):
    """Busca um vínculo por ID."""
    return db.query(models.VeiculoPlano).filter(models.VeiculoPlano.id == veiculo_plano_id).first()


def get_veiculos_do_plano(db: Session, plano_id: int):
    """Lista todos os veículos vinculados a um plano."""
    return db.query(models.VeiculoPlano)\
        .filter(models.VeiculoPlano.plano_manutencao_id == plano_id)\
        .all()


def get_planos_do_veiculo(db: Session, veiculo_id: int):
    """Lista todos os planos vinculados a um veículo."""
    return db.query(models.VeiculoPlano)\
        .filter(models.VeiculoPlano.veiculo_id == veiculo_id)\
        .all()


def vincular_veiculo_plano(db: Session, veiculo_id: int, plano_id: int, data_inicio: date):
    """Vincula um veículo a um plano."""
    db_vinculo = models.VeiculoPlano(
        veiculo_id=veiculo_id,
        plano_manutencao_id=plano_id,
        data_inicio=data_inicio,
        ativo=True
    )
    db.add(db_vinculo)
    db.commit()
    db.refresh(db_vinculo)
    return db_vinculo


def desvincular_veiculo_plano(db: Session, veiculo_id: int, plano_id: int):
    """Remove o vínculo entre veículo e plano."""
    db_vinculo = db.query(models.VeiculoPlano)\
        .filter(models.VeiculoPlano.veiculo_id == veiculo_id)\
        .filter(models.VeiculoPlano.plano_manutencao_id == plano_id)\
        .first()
    
    if not db_vinculo:
        return False
    
    db.delete(db_vinculo)
    db.commit()
    return True


def update_veiculo_plano(db: Session, veiculo_plano_id: int, vinculo: schemas.VeiculoPlanoUpdate):
    """Atualiza um vínculo existente."""
    db_vinculo = get_veiculo_plano(db, veiculo_plano_id)
    if not db_vinculo:
        return None
    
    update_data = vinculo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vinculo, key, value)
    
    db.commit()
    db.refresh(db_vinculo)
    return db_vinculo
