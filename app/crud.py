from sqlalchemy.orm import Session
from app import models, schemas

# ============================================================
# 1. CRUD de USUÁRIO
# ============================================================

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Cria um novo usuário no banco."""
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=usuario.senha  # Em produção, utilize gerar_hash_senha(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


def listar_usuarios(db: Session):
    """Retorna todos os usuários cadastrados."""
    return db.query(models.Usuario).all()


def buscar_usuario_por_email(db: Session, email: str):
    """Busca um usuário pelo e-mail."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


# ============================================================
# 2. CRUD de VEÍCULO
# ============================================================

def criar_veiculo(db: Session, veiculo: schemas.VeiculoCreate):
    """Cria um novo veículo vinculado a um usuário."""
    novo_veiculo = models.Veiculo(**veiculo.model_dump())
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)
    return novo_veiculo


def listar_veiculos(db: Session):
    """Lista todos os veículos cadastrados."""
    return db.query(models.Veiculo).all()


def buscar_veiculo_por_id(db: Session, veiculo_id: int):
    """Busca um veículo pelo ID."""
    return db.query(models.Veiculo).filter(models.Veiculo.id == veiculo_id).first()


def atualizar_veiculo(db: Session, veiculo_id: int, dados: schemas.VeiculoBase):
    """Atualiza os dados de um veículo existente."""
    veiculo = buscar_veiculo_por_id(db, veiculo_id)
    if not veiculo:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(veiculo, campo, valor)
    db.commit()
    db.refresh(veiculo)
    return veiculo


def excluir_veiculo(db: Session, veiculo_id: int):
    """Remove um veículo do banco."""
    veiculo = buscar_veiculo_por_id(db, veiculo_id)
    if not veiculo:
        return None
    db.delete(veiculo)
    db.commit()
    return veiculo


# ============================================================
# 3. CRUD de MANUTENÇÃO
# ============================================================

def criar_manutencao(db: Session, manutencao: schemas.ManutencaoCreate):
    """Cria um registro de manutenção."""
    nova_manutencao = models.Manutencao(**manutencao.model_dump())
    db.add(nova_manutencao)
    db.commit()
    db.refresh(nova_manutencao)
    return nova_manutencao


def listar_manutencoes(db: Session):
    """Lista todas as manutenções."""
    return db.query(models.Manutencao).all()


def buscar_manutencao_por_id(db: Session, manutencao_id: int):
    """Busca uma manutenção específica."""
    return db.query(models.Manutencao).filter(models.Manutencao.id == manutencao_id).first()


def excluir_manutencao(db: Session, manutencao_id: int):
    """Exclui uma manutenção."""
    manutencao = buscar_manutencao_por_id(db, manutencao_id)
    if manutencao:
        db.delete(manutencao)
        db.commit()
        return manutencao
    return None


# ============================================================
# 4. CRUD de DOCUMENTOS
# ============================================================

def criar_documento(db: Session, documento: schemas.DocumentoCreate):
    """Salva o registro de um documento vinculado a uma manutenção."""
    novo_documento = models.Documento(**documento.model_dump())
    db.add(novo_documento)
    db.commit()
    db.refresh(novo_documento)
    return novo_documento


def listar_documentos(db: Session):
    """Lista todos os documentos cadastrados."""
    return db.query(models.Documento).all()


def excluir_documento(db: Session, documento_id: int):
    """Remove um documento."""
    doc = db.query(models.Documento).filter(models.Documento.id == documento_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return doc
    return None


# ============================================================
# 5. CRUD de PLANOS DE MANUTENÇÃO
# ============================================================

def criar_plano(db: Session, plano: schemas.PlanoManutencaoCreate):
    """Cria um plano de manutenção para um veículo."""
    novo_plano = models.PlanoManutencao(**plano.model_dump())
    db.add(novo_plano)
    db.commit()
    db.refresh(novo_plano)
    return novo_plano


def listar_planos(db: Session):
    """Lista todos os planos de manutenção."""
    return db.query(models.PlanoManutencao).all()


def excluir_plano(db: Session, plano_id: int):
    """Exclui um plano de manutenção."""
    plano = db.query(models.PlanoManutencao).filter(models.PlanoManutencao.id == plano_id).first()
    if plano:
        db.delete(plano)
        db.commit()
        return plano
    return None
