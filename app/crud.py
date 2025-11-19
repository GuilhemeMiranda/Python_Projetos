from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models, schemas
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
# CRUD de Planos de Manutenção
# ============================================================

def get_plano_manutencao(db: Session, plano_id: int):
    """Busca um plano de manutenção por ID."""
    result = db.execute(
        text("SELECT * FROM planos_manutencao WHERE id = :id"),
        {"id": plano_id}
    ).fetchone()
    return result

def get_planos_manutencao(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos os planos de manutenção."""
    result = db.execute(
        text("SELECT * FROM planos_manutencao LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip}
    ).fetchall()
    return result

def create_plano_manutencao(db: Session, plano: schemas.PlanoManutencaoCreate):
    """Cria um novo plano de manutenção."""
    db.execute(
        text("""
            INSERT INTO planos_manutencao 
            (veiculo_id, tipo_manutencao, km_proxima, data_proxima, periodicidade_km, periodicidade_meses, descricao)
            VALUES (:veiculo_id, :tipo_manutencao, :km_proxima, :data_proxima, :periodicidade_km, :periodicidade_meses, :descricao)
        """),
        {
            "veiculo_id": plano.veiculo_id,
            "tipo_manutencao": plano.tipo_manutencao,
            "km_proxima": plano.km_proxima,
            "data_proxima": plano.data_proxima,
            "periodicidade_km": plano.periodicidade_km,
            "periodicidade_meses": plano.periodicidade_meses,
            "descricao": plano.descricao
        }
    )
    db.commit()
    
    result = db.execute(
        text("SELECT * FROM planos_manutencao WHERE veiculo_id = :veiculo_id ORDER BY id DESC LIMIT 1"),
        {"veiculo_id": plano.veiculo_id}
    ).fetchone()
    return result

def update_plano_manutencao(db: Session, plano_id: int, plano: schemas.PlanoManutencaoUpdate):
    """Atualiza um plano de manutenção."""
    update_fields = []
    params = {"id": plano_id}
    
    if plano.tipo_manutencao is not None:
        update_fields.append("tipo_manutencao = :tipo_manutencao")
        params["tipo_manutencao"] = plano.tipo_manutencao
    
    if plano.km_proxima is not None:
        update_fields.append("km_proxima = :km_proxima")
        params["km_proxima"] = plano.km_proxima
    
    if plano.data_proxima is not None:
        update_fields.append("data_proxima = :data_proxima")
        params["data_proxima"] = plano.data_proxima
    
    if plano.periodicidade_km is not None:
        update_fields.append("periodicidade_km = :periodicidade_km")
        params["periodicidade_km"] = plano.periodicidade_km
    
    if plano.periodicidade_meses is not None:
        update_fields.append("periodicidade_meses = :periodicidade_meses")
        params["periodicidade_meses"] = plano.periodicidade_meses
    
    if plano.descricao is not None:
        update_fields.append("descricao = :descricao")
        params["descricao"] = plano.descricao
    
    if not update_fields:
        return get_plano_manutencao(db, plano_id)
    
    query = f"UPDATE planos_manutencao SET {', '.join(update_fields)} WHERE id = :id"
    
    db.execute(text(query), params)
    db.commit()
    
    return get_plano_manutencao(db, plano_id)

def delete_plano_manutencao(db: Session, plano_id: int):
    """Deleta um plano de manutenção."""
    db.execute(
        text("DELETE FROM planos_manutencao WHERE id = :id"),
        {"id": plano_id}
    )
    db.commit()
    return True
