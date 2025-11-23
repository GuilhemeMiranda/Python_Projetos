"""
Testes para os endpoints de veículos.
"""

import pytest
from fastapi import status


def test_criar_veiculo(client, usuario_data, veiculo_data):
    """Testa a criação de um novo veículo."""
    # Primeiro criar um usuário
    client.post("/usuarios/", json=usuario_data)
    
    # Criar veículo
    response = client.post("/veiculos/", json=veiculo_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["placa"] == veiculo_data["placa"]
    assert data["modelo"] == veiculo_data["modelo"]
    assert "id" in data


def test_listar_veiculos(client, usuario_data, veiculo_data):
    """Testa a listagem de veículos."""
    # Criar usuário e veículos
    client.post("/usuarios/", json=usuario_data)
    client.post("/veiculos/", json=veiculo_data)
    
    veiculo_data2 = veiculo_data.copy()
    veiculo_data2["placa"] = "XYZ-9876"
    veiculo_data2["modelo"] = "Corolla"
    client.post("/veiculos/", json=veiculo_data2)
    
    # Listar veículos
    response = client.get("/veiculos/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_buscar_veiculo_por_id(client, usuario_data, veiculo_data):
    """Testa a busca de veículo por ID."""
    # Criar usuário e veículo
    client.post("/usuarios/", json=usuario_data)
    response_create = client.post("/veiculos/", json=veiculo_data)
    veiculo_id = response_create.json()["id"]
    
    # Buscar veículo
    response = client.get(f"/veiculos/{veiculo_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == veiculo_id
    assert data["placa"] == veiculo_data["placa"]


def test_buscar_veiculo_inexistente(client):
    """Testa busca de veículo que não existe."""
    response = client.get("/veiculos/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_atualizar_veiculo(client, usuario_data, veiculo_data):
    """Testa a atualização de um veículo."""
    # Criar usuário e veículo
    client.post("/usuarios/", json=usuario_data)
    response_create = client.post("/veiculos/", json=veiculo_data)
    veiculo_id = response_create.json()["id"]
    
    # Atualizar veículo
    dados_atualizados = {
        "placa": veiculo_data["placa"],
        "modelo": veiculo_data["modelo"],
        "marca": veiculo_data["marca"],
        "ano": veiculo_data["ano"],
        "km_atual": 20000  # Atualizar quilometragem
    }
    response = client.put(f"/veiculos/{veiculo_id}", json=dados_atualizados)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["km_atual"] == 20000


def test_excluir_veiculo(client, usuario_data, veiculo_data):
    """Testa a exclusão de um veículo."""
    # Criar usuário e veículo
    client.post("/usuarios/", json=usuario_data)
    response_create = client.post("/veiculos/", json=veiculo_data)
    veiculo_id = response_create.json()["id"]
    
    # Excluir veículo
    response = client.delete(f"/veiculos/{veiculo_id}")
    
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que foi excluído
    response_get = client.get(f"/veiculos/{veiculo_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND


def test_excluir_veiculo_inexistente(client):
    """Testa exclusão de veículo que não existe."""
    response = client.delete("/veiculos/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
