"""
Testes para o endpoint raiz e estrutura geral da API.
"""

from fastapi import status


def test_home_endpoint(client):
    """Testa o endpoint raiz da API."""
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "mensagem" in data
    assert "Bem-vindo" in data["mensagem"]


def test_docs_disponivel(client):
    """Testa que a documentação Swagger está disponível."""
    response = client.get("/docs")
    
    assert response.status_code == status.HTTP_200_OK


def test_openapi_schema_disponivel(client):
    """Testa que o schema OpenAPI está disponível."""
    response = client.get("/openapi.json")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "API - Minha Manutenção Veicular"
