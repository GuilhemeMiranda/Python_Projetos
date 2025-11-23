# Configuração do pytest para o projeto

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

# =================================================================
# Configuração do banco de dados de teste
# =================================================================

# Usar banco SQLite em memória para testes
TEST_DATABASE_URL = "sqlite:///./test_manutencao_veicular.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# =================================================================
# Fixtures
# =================================================================

@pytest.fixture(scope="function")
def db():
    """
    Cria um banco de dados de teste limpo para cada teste.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Cliente de teste FastAPI com banco de dados sobrescrito.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_data():
    """Dados de exemplo para criar um usuário."""
    return {
        "nome": "João Silva",
        "email": "joao@exemplo.com",
        "senha": "senha123"
    }


@pytest.fixture
def veiculo_data():
    """Dados de exemplo para criar um veículo."""
    return {
        "placa": "ABC-1234",
        "modelo": "Civic",
        "marca": "Honda",
        "ano": 2020,
        "km_atual": 15000,
        "usuario_id": 1
    }


@pytest.fixture
def manutencao_data():
    """Dados de exemplo para criar uma manutenção."""
    return {
        "veiculo_id": 1,
        "data": "2024-01-15",
        "km": 15000,
        "tipo_manutencao": "Troca de óleo",
        "descricao": "Troca de óleo e filtro",
        "custo": 150.00,
        "prestador_servico": "AutoCenter Silva"
    }


@pytest.fixture
def plano_data():
    """Dados de exemplo para criar um plano de manutenção."""
    return {
        "veiculo_id": 1,
        "nome_plano": "Manutenção 10.000 km",
        "km_referencia": 10000,
        "servicos": "Troca de óleo, filtro de ar, revisão geral"
    }
