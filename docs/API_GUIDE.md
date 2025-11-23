# Guia da API - Manutenção Veicular

Documentação completa dos endpoints da API de Manutenção Veicular.

## 📖 Informações Gerais

**Base URL:** `http://localhost:8000`

**Formato de Resposta:** JSON

**Autenticação:** Bearer Token (JWT) - *A ser implementado*

## 🚀 Início Rápido

### 1. Iniciar o Servidor

```bash
uvicorn app.main:app --reload
```

### 2. Acessar Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 3. Testar Endpoint

```bash
curl http://localhost:8000/
```

## 📍 Endpoints

### 🏠 Raiz

#### GET `/`

Endpoint de boas-vindas.

**Response:**
```json
{
  "mensagem": "Bem-vindo à API de Manutenção Veicular 🚗"
}
```

---

## 👤 Usuários

### POST `/usuarios/`

Cria um novo usuário.

**Request Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@exemplo.com",
  "senha": "senha123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@exemplo.com"
}
```

**Erros:**
- `400 Bad Request` - Email já cadastrado
- `422 Unprocessable Entity` - Dados inválidos

### GET `/usuarios/`

Lista todos os usuários.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@exemplo.com"
  },
  {
    "id": 2,
    "nome": "Maria Santos",
    "email": "maria@exemplo.com"
  }
]
```

### GET `/usuarios/buscar?email={email}`

Busca usuário por email.

**Query Parameters:**
- `email` (required): Email do usuário

**Response (200 OK):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@exemplo.com"
}
```

**Erros:**
- `404 Not Found` - Usuário não encontrado

---

## 🚗 Veículos

### POST `/veiculos/`

Cadastra um novo veículo.

**Request Body:**
```json
{
  "placa": "ABC-1234",
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2020,
  "km_atual": 15000,
  "usuario_id": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2020,
  "km_atual": 15000,
  "usuario_id": 1
}
```

### GET `/veiculos/`

Lista todos os veículos.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "placa": "ABC-1234",
    "modelo": "Civic",
    "marca": "Honda",
    "ano": 2020,
    "km_atual": 15000,
    "usuario_id": 1
  }
]
```

### GET `/veiculos/{id}`

Busca veículo por ID.

**Path Parameters:**
- `id` (required): ID do veículo

**Response (200 OK):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2020,
  "km_atual": 15000,
  "usuario_id": 1
}
```

**Erros:**
- `404 Not Found` - Veículo não encontrado

### PUT `/veiculos/{id}`

Atualiza dados do veículo.

**Path Parameters:**
- `id` (required): ID do veículo

**Request Body:**
```json
{
  "placa": "ABC-1234",
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2020,
  "km_atual": 20000
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2020,
  "km_atual": 20000,
  "usuario_id": 1
}
```

### DELETE `/veiculos/{id}`

Exclui um veículo.

**Path Parameters:**
- `id` (required): ID do veículo

**Response (200 OK):**
```json
{
  "id": 1,
  "placa": "ABC-1234",
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2020,
  "km_atual": 15000,
  "usuario_id": 1
}
```

---

## 🔧 Manutenções

### POST `/manutencoes/`

Registra uma nova manutenção.

**Request Body:**
```json
{
  "veiculo_id": 1,
  "data": "2024-01-15",
  "km": 15000,
  "tipo_manutencao": "Troca de óleo",
  "descricao": "Troca de óleo e filtro",
  "custo": 150.00,
  "prestador_servico": "AutoCenter Silva"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "veiculo_id": 1,
  "data": "2024-01-15",
  "km": 15000,
  "tipo_manutencao": "Troca de óleo",
  "descricao": "Troca de óleo e filtro",
  "custo": 150.00,
  "prestador_servico": "AutoCenter Silva"
}
```

**Erros:**
- `404 Not Found` - Veículo não encontrado

### GET `/manutencoes/`

Lista todas as manutenções.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "veiculo_id": 1,
    "data": "2024-01-15",
    "km": 15000,
    "tipo_manutencao": "Troca de óleo",
    "descricao": "Troca de óleo e filtro",
    "custo": 150.00,
    "prestador_servico": "AutoCenter Silva"
  }
]
```

### GET `/manutencoes/{id}`

Busca manutenção por ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "veiculo_id": 1,
  "data": "2024-01-15",
  "km": 15000,
  "tipo_manutencao": "Troca de óleo",
  "descricao": "Troca de óleo e filtro",
  "custo": 150.00,
  "prestador_servico": "AutoCenter Silva"
}
```

### DELETE `/manutencoes/{id}`

Remove uma manutenção.

**Response (200 OK):**
```json
{
  "id": 1,
  "veiculo_id": 1,
  "data": "2024-01-15",
  "km": 15000,
  "tipo_manutencao": "Troca de óleo",
  "descricao": "Troca de óleo e filtro",
  "custo": 150.00,
  "prestador_servico": "AutoCenter Silva"
}
```

---

## 📅 Planos de Manutenção

### POST `/planos/`

Cria um plano de manutenção.

**Request Body:**
```json
{
  "veiculo_id": 1,
  "nome_plano": "Manutenção 10.000 km",
  "km_referencia": 10000,
  "servicos": "Troca de óleo, filtro de ar, revisão geral"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "veiculo_id": 1,
  "nome_plano": "Manutenção 10.000 km",
  "km_referencia": 10000,
  "servicos": "Troca de óleo, filtro de ar, revisão geral"
}
```

### GET `/planos/`

Lista todos os planos.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "veiculo_id": 1,
    "nome_plano": "Manutenção 10.000 km",
    "km_referencia": 10000,
    "servicos": "Troca de óleo, filtro de ar, revisão geral"
  }
]
```

### GET `/planos/veiculo/{veiculo_id}`

Lista planos de um veículo específico.

**Path Parameters:**
- `veiculo_id` (required): ID do veículo

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "veiculo_id": 1,
    "nome_plano": "Manutenção 10.000 km",
    "km_referencia": 10000,
    "servicos": "Troca de óleo, filtro de ar, revisão geral"
  }
]
```

### DELETE `/planos/{id}`

Remove um plano.

**Response (200 OK):**
```json
{
  "id": 1,
  "veiculo_id": 1,
  "nome_plano": "Manutenção 10.000 km",
  "km_referencia": 10000,
  "servicos": "Troca de óleo, filtro de ar, revisão geral"
}
```

---

## 🔒 Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Dados inválidos ou duplicados |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Erro de validação |
| 500 | Internal Server Error - Erro no servidor |

## 📝 Exemplos com cURL

### Criar Usuário
```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "senha": "senha123"
  }'
```

### Listar Veículos
```bash
curl -X GET "http://localhost:8000/veiculos/"
```

### Atualizar Veículo
```bash
curl -X PUT "http://localhost:8000/veiculos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "modelo": "Civic",
    "marca": "Honda",
    "ano": 2020,
    "km_atual": 20000
  }'
```

## 🐍 Exemplos com Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Criar usuário
response = requests.post(
    f"{BASE_URL}/usuarios/",
    json={
        "nome": "João Silva",
        "email": "joao@exemplo.com",
        "senha": "senha123"
    }
)
print(response.json())

# Listar veículos
response = requests.get(f"{BASE_URL}/veiculos/")
print(response.json())

# Criar manutenção
response = requests.post(
    f"{BASE_URL}/manutencoes/",
    json={
        "veiculo_id": 1,
        "data": "2024-01-15",
        "km": 15000,
        "tipo_manutencao": "Troca de óleo",
        "descricao": "Troca de óleo e filtro",
        "custo": 150.00,
        "prestador_servico": "AutoCenter Silva"
    }
)
print(response.json())
```

## 📦 Paginação (Futuro)

*A ser implementado na versão 2.0*

```
GET /veiculos/?page=1&limit=10
```

## 🔍 Filtros (Futuro)

*A ser implementado na versão 2.0*

```
GET /manutencoes/?veiculo_id=1&data_inicio=2024-01-01&data_fim=2024-12-31
```

## 🌐 CORS

A API está configurada para aceitar requisições de:
- `http://localhost:3000`
- Configure origens adicionais no arquivo `.env`

## 📚 Recursos Adicionais

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

---

**Versão da API:** 1.0.0  
**Última atualização:** Novembro 2024
