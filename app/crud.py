from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from typing import Optional, List

# ===== CRUD DE USUÁRIOS =====
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    from app.security import gerar_hash_senha
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def atualizar_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    from app.security import gerar_hash_senha
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db_usuario.nome = usuario.nome
        db_usuario.email = usuario.email
        if usuario.senha:
            db_usuario.senha_hash = gerar_hash_senha(usuario.senha)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def deletar_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

# ===== CRUD DE VEÍCULOS =====
def criar_veiculo(db: Session, veiculo: schemas.VeiculoCreate, usuario_id: int):
    db_veiculo = models.Veiculo(
        placa=veiculo.placa,
        ano=veiculo.ano,
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        km_atual=veiculo.km_atual,
        usuario_id=usuario_id
    )
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

def get_veiculo(db: Session, veiculo_id: int):
    return db.query(models.Veiculo).filter(models.Veiculo.id == veiculo_id).first()

def get_veiculo_por_placa(db: Session, placa: str):
    return db.query(models.Veiculo).filter(models.Veiculo.placa == placa).first()

def get_veiculos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Veiculo).offset(skip).limit(limit).all()

def get_veiculos_usuario(db: Session, usuario_id: int):
    return db.query(models.Veiculo).filter(models.Veiculo.usuario_id == usuario_id).all()

def atualizar_veiculo(db: Session, veiculo_id: int, veiculo: schemas.VeiculoCreate):
    db_veiculo = get_veiculo(db, veiculo_id)
    if db_veiculo:
        db_veiculo.placa = veiculo.placa
        db_veiculo.ano = veiculo.ano
        db_veiculo.marca = veiculo.marca
        db_veiculo.modelo = veiculo.modelo
        db_veiculo.km_atual = veiculo.km_atual
        db.commit()
        db.refresh(db_veiculo)
    return db_veiculo

def deletar_veiculo(db: Session, veiculo_id: int):
    db_veiculo = get_veiculo(db, veiculo_id)
    if db_veiculo:
        db.delete(db_veiculo)
        db.commit()
    return db_veiculo

# ===== CRUD DE MANUTENÇÕES =====
def criar_manutencao(db: Session, manutencao: schemas.ManutencaoCreate):
    db_manutencao = models.Manutencao(
        veiculo_id=manutencao.veiculo_id,
        data=manutencao.data,
        km=manutencao.km,
        tipo=manutencao.tipo,
        prestador=manutencao.prestador,
        custo=manutencao.custo
    )
    db.add(db_manutencao)
    db.commit()
    db.refresh(db_manutencao)
    return db_manutencao

def get_manutencao(db: Session, manutencao_id: int):
    return db.query(models.Manutencao).filter(models.Manutencao.id == manutencao_id).first()

def get_manutencoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Manutencao).offset(skip).limit(limit).all()

def get_manutencoes_veiculo(db: Session, veiculo_id: int):
    return db.query(models.Manutencao).filter(
        models.Manutencao.veiculo_id == veiculo_id
    ).order_by(models.Manutencao.data.desc()).all()

def atualizar_manutencao(db: Session, manutencao_id: int, manutencao: schemas.ManutencaoCreate):
    db_manutencao = get_manutencao(db, manutencao_id)
    if db_manutencao:
        db_manutencao.veiculo_id = manutencao.veiculo_id
        db_manutencao.data = manutencao.data
        db_manutencao.km = manutencao.km
        db_manutencao.tipo = manutencao.tipo
        db_manutencao.prestador = manutencao.prestador
        db_manutencao.custo = manutencao.custo
        db.commit()
        db.refresh(db_manutencao)
    return db_manutencao

def deletar_manutencao(db: Session, manutencao_id: int):
    db_manutencao = get_manutencao(db, manutencao_id)
    if db_manutencao:
        db.delete(db_manutencao)
        db.commit()
    return db_manutencao

# ===== CRUD DE PLANOS DE MANUTENÇÃO =====
def criar_plano(db: Session, plano: schemas.PlanoCreate):
    db_plano = models.PlanoManutencao(
        veiculo_id=plano.veiculo_id,
        tipo_manutencao=plano.tipo_manutencao,
        km_previsto=plano.km_previsto,
        data_prevista=plano.data_prevista
    )
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

def get_plano(db: Session, plano_id: int):
    return db.query(models.PlanoManutencao).filter(models.PlanoManutencao.id == plano_id).first()

def get_planos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PlanoManutencao).offset(skip).limit(limit).all()

def get_planos_veiculo(db: Session, veiculo_id: int):
    return db.query(models.PlanoManutencao).filter(
        models.PlanoManutencao.veiculo_id == veiculo_id
    ).order_by(models.PlanoManutencao.km_previsto).all()

def atualizar_plano(db: Session, plano_id: int, plano: schemas.PlanoCreate):
    db_plano = get_plano(db, plano_id)
    if db_plano:
        db_plano.veiculo_id = plano.veiculo_id
        db_plano.tipo_manutencao = plano.tipo_manutencao
        db_plano.km_previsto = plano.km_previsto
        db_plano.data_prevista = plano.data_prevista
        db.commit()
        db.refresh(db_plano)
    return db_plano

def deletar_plano(db: Session, plano_id: int):
    db_plano = get_plano(db, plano_id)
    if db_plano:
        db.delete(db_plano)
        db.commit()
    return db_plano
