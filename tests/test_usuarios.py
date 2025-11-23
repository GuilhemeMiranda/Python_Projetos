"""
Testes para os endpoints de usuários.
"""

import pytest
from fastapi import status


def test_criar_usuario(client, usuario_data):
    """Testa a criação de um novo usuário."""
    response = client.post("/usuarios/", json=usuario_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == usuario_data["nome"]
    assert data["email"] == usuario_data["email"]
    assert "id" in data
    assert "senha" not in data  # Senha não deve ser retornada


def test_criar_usuario_email_duplicado(client, usuario_data):
    """Testa que não é possível criar usuário com email duplicado."""
    # Criar primeiro usuário
    client.post("/usuarios/", json=usuario_data)
    
    # Tentar criar segundo usuário com mesmo email
    response = client.post("/usuarios/", json=usuario_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "já cadastrado" in response.json()["detail"].lower()


def test_listar_usuarios(client, usuario_data):
    """Testa a listagem de usuários."""
    # Criar alguns usuários
    client.post("/usuarios/", json=usuario_data)
    
    usuario_data2 = usuario_data.copy()
    usuario_data2["email"] = "maria@exemplo.com"
    usuario_data2["nome"] = "Maria Santos"
    client.post("/usuarios/", json=usuario_data2)
    
    # Listar usuários
    response = client.get("/usuarios/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == usuario_data["nome"]
    assert data[1]["nome"] == usuario_data2["nome"]


def test_buscar_usuario_por_email(client, usuario_data):
    """Testa a busca de usuário por email."""
    # Criar usuário
    client.post("/usuarios/", json=usuario_data)
    
    # Buscar usuário
    response = client.get(f"/usuarios/buscar?email={usuario_data['email']}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == usuario_data["email"]
    assert data["nome"] == usuario_data["nome"]


def test_buscar_usuario_inexistente(client):
    """Testa busca de usuário que não existe."""
    response = client.get("/usuarios/buscar?email=naoexiste@exemplo.com")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_criar_usuario_sem_dados_obrigatorios(client):
    """Testa que não é possível criar usuário sem dados obrigatórios."""
    response = client.post("/usuarios/", json={})
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_criar_usuario_email_invalido(client):
    """Testa que não é possível criar usuário com email inválido."""
    usuario_invalido = {
        "nome": "Teste",
        "email": "email-invalido",
        "senha": "senha123"
    }
    response = client.post("/usuarios/", json=usuario_invalido)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
