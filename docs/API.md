# 🔌 Documentação da API - Sistema de Manutenção Veicular

Documentação completa da API REST do Sistema de Manutenção Veicular.

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Autenticação](#-autenticação)
3. [Endpoints de Autenticação](#-endpoints-de-autenticação)
4. [Endpoints de Veículos](#-endpoints-de-veículos)
5. [Endpoints de Manutenções](#-endpoints-de-manutenções)
6. [Endpoints de Usuários](#-endpoints-de-usuários)
7. [Endpoints de Planos](#-endpoints-de-planos)
8. [Modelos de Dados](#-modelos-de-dados)
9. [Códigos de Status](#-códigos-de-status)
10. [Exemplos de Uso](#-exemplos-de-uso)
11. [Tratamento de Erros](#-tratamento-de-erros)

---

## 🎯 Visão Geral

### Base URL

```
http://localhost:8000
```

### Formato de Dados

- **Request:** JSON
- **Response:** JSON
- **Encoding:** UTF-8

### Versionamento

- **Versão Atual:** 1.3.0
- **API Version:** v1 (implícita)

### Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Como Funciona

1. **Login:** Envie credenciais para `/auth/login`
2. **Token:** Receba um token JWT
3. **Uso:** Envie o token no header `Authorization` ou cookie `access_token`
4. **Expiração:** Token expira em 30 minutos (configurável)

### Formato do Token

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Headers Necessários

```http
Authorization: Bearer {seu_token_aqui}
Content-Type: application/json
```

### Cookie (Alternativa)

O sistema também aceita o token via cookie `access_token` (httpOnly).

---

## 🔑 Endpoints de Autenticação

### 1. Registrar Novo Usuário

Cria uma nova conta de usuário.

```http
POST /auth/register
```

**Request Body:**

```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senha123"
}
```

**Response: 201 Created**

```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "plano_id": 1,
  "created_at": "2024-11-19T10:30:00"
}
```

**Erros Possíveis:**

- `400 Bad Request` - Email já cadastrado
- `422 Unprocessable Entity` - Dados inválidos

---

### 2. Login

Autentica um usuário e retorna um token JWT.

```http
POST /auth/login
```

**Request Body (Form Data):**

```
username: joao@email.com
password: senha123
```

**Response: 200 OK**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**O token também é definido como cookie httpOnly.**

**Erros Possíveis:**

- `401 Unauthorized` - Credenciais inválidas
- `422 Unprocessable Entity` - Dados faltando

---

### 3. Logout

Invalida o token atual.

```http
POST /auth/logout
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "message": "Logout realizado com sucesso"
}
```

---

### 4. Obter Usuário Atual

Retorna os dados do usuário autenticado.

```http
GET /auth/me
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "plano_id": 1,
  "created_at": "2024-11-19T10:30:00"
}
```

---

## 🚗 Endpoints de Veículos

### 1. Listar Veículos do Usuário

Retorna todos os veículos do usuário autenticado.

```http
GET /veiculos/
```

**Headers:**

```
Authorization: Bearer {token}
```

**Query Parameters (Opcional):**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `placa` | string | Filtrar por placa |
| `skip` | int | Paginação: itens para pular (padrão: 0) |
| `limit` | int | Paginação: máximo de itens (padrão: 100) |

**Exemplo:**

```http
GET /veiculos/?placa=ABC1234
```

**Response: 200 OK**

```json
[
  {
    "id": 1,
    "placa": "ABC1234",
    "marca": "Ford",
    "modelo": "Fiesta",
    "ano": 2020,
    "km_atual": 45000,
    "usuario_id": 1,
    "created_at": "2024-11-19T10:30:00"
  },
  {
    "id": 2,
    "placa": "XYZ5678",
    "marca": "Fiat",
    "modelo": "Uno",
    "ano": 2018,
    "km_atual": 78000,
    "usuario_id": 1,
    "created_at": "2024-11-15T14:20:00"
  }
]
```

---

### 2. Criar Novo Veículo

Cadastra um novo veículo para o usuário autenticado.

```http
POST /veiculos/
```

**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "placa": "ABC1234",
  "marca": "Ford",
  "modelo": "Fiesta",
  "ano": 2020,
  "km_atual": 45000
}
```

**Validações:**

- `placa`: Deve ser única, formato: ABC1234 ou ABC-1234
- `ano`: Entre 1900 e ano atual
- `km_atual`: Número positivo

**Response: 201 Created**

```json
{
  "id": 1,
  "placa": "ABC1234",
  "marca": "Ford",
  "modelo": "Fiesta",
  "ano": 2020,
  "km_atual": 45000,
  "usuario_id": 1,
  "created_at": "2024-11-19T10:30:00"
}
```

**Erros Possíveis:**

- `400 Bad Request` - Placa já cadastrada
- `422 Unprocessable Entity` - Dados inválidos

---

### 3. Buscar Veículo por ID

Retorna os detalhes de um veículo específico.

```http
GET /veiculos/{veiculo_id}
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "id": 1,
  "placa": "ABC1234",
  "marca": "Ford",
  "modelo": "Fiesta",
  "ano": 2020,
  "km_atual": 45000,
  "usuario_id": 1,
  "created_at": "2024-11-19T10:30:00"
}
```

**Erros Possíveis:**

- `404 Not Found` - Veículo não encontrado
- `403 Forbidden` - Veículo não pertence ao usuário

---

### 4. Atualizar Veículo

Atualiza os dados de um veículo.

```http
PUT /veiculos/{veiculo_id}
```

**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "marca": "Ford",
  "modelo": "Fiesta 1.6",
  "ano": 2020,
  "km_atual": 48000
}
```

**⚠️ Nota:** A placa **não** pode ser alterada.

**Response: 200 OK**

```json
{
  "id": 1,
  "placa": "ABC1234",
  "marca": "Ford",
  "modelo": "Fiesta 1.6",
  "ano": 2020,
  "km_atual": 48000,
  "usuario_id": 1,
  "created_at": "2024-11-19T10:30:00"
}
```

**Erros Possíveis:**

- `404 Not Found` - Veículo não encontrado
- `403 Forbidden` - Veículo não pertence ao usuário
- `422 Unprocessable Entity` - Dados inválidos

---

### 5. Deletar Veículo

Remove um veículo do sistema.

```http
DELETE /veiculos/{veiculo_id}
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "message": "Veículo deletado com sucesso",
  "id": 1
}
```

**⚠️ Atenção:** Todas as manutenções associadas também serão deletadas!

**Erros Possíveis:**

- `404 Not Found` - Veículo não encontrado
- `403 Forbidden` - Veículo não pertence ao usuário

---

## 🔧 Endpoints de Manutenções

### 1. Listar Manutenções

Retorna todas as manutenções dos veículos do usuário.

```http
GET /manutencoes/
```

**Headers:**

```
Authorization: Bearer {token}
```

**Query Parameters (Opcional):**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `veiculo_id` | int | Filtrar por veículo |
| `placa` | string | Filtrar por placa |
| `skip` | int | Paginação: itens para pular |
| `limit` | int | Paginação: máximo de itens |

**Exemplo:**

```http
GET /manutencoes/?placa=ABC1234
```

**Response: 200 OK**

```json
[
  {
    "id": 1,
    "veiculo_id": 1,
    "data_manutencao": "2024-11-15",
    "km_manutencao": 45000,
    "tipo_manutencao": "Troca de óleo",
    "prestador_servico": "Oficina XYZ",
    "custo": 150.00,
    "observacoes": "Óleo sintético 5W30",
    "created_at": "2024-11-15T14:20:00",
    "veiculo": {
      "placa": "ABC1234",
      "marca": "Ford",
      "modelo": "Fiesta"
    }
  }
]
```

---

### 2. Criar Manutenção

Registra uma nova manutenção.

```http
POST /manutencoes/
```

**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "veiculo_id": 1,
  "data_manutencao": "2024-11-15",
  "km_manutencao": 45000,
  "tipo_manutencao": "Troca de óleo",
  "prestador_servico": "Oficina XYZ",
  "custo": 150.00,
  "observacoes": "Óleo sintético 5W30"
}
```

**Validações:**

- `data_manutencao`: Não pode ser futura
- `km_manutencao`: Deve ser >= km_atual do veículo
- `custo`: Número positivo
- `observacoes`: Opcional

**Response: 201 Created**

```json
{
  "id": 1,
  "veiculo_id": 1,
  "data_manutencao": "2024-11-15",
  "km_manutencao": 45000,
  "tipo_manutencao": "Troca de óleo",
  "prestador_servico": "Oficina XYZ",
  "custo": 150.00,
  "observacoes": "Óleo sintético 5W30",
  "created_at": "2024-11-15T14:20:00"
}
```

**Erros Possíveis:**

- `404 Not Found` - Veículo não encontrado
- `403 Forbidden` - Veículo não pertence ao usuário
- `400 Bad Request` - KM menor que KM atual do veículo
- `422 Unprocessable Entity` - Dados inválidos

---

### 3. Buscar Manutenção por ID

Retorna os detalhes de uma manutenção específica.

```http
GET /manutencoes/{manutencao_id}
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "id": 1,
  "veiculo_id": 1,
  "data_manutencao": "2024-11-15",
  "km_manutencao": 45000,
  "tipo_manutencao": "Troca de óleo",
  "prestador_servico": "Oficina XYZ",
  "custo": 150.00,
  "observacoes": "Óleo sintético 5W30",
  "created_at": "2024-11-15T14:20:00",
  "veiculo": {
    "placa": "ABC1234",
    "marca": "Ford",
    "modelo": "Fiesta"
  }
}
```

---

### 4. Atualizar Manutenção

Atualiza os dados de uma manutenção.

```http
PUT /manutencoes/{manutencao_id}
```

**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "data_manutencao": "2024-11-15",
  "km_manutencao": 45000,
  "tipo_manutencao": "Troca de óleo e filtros",
  "prestador_servico": "Oficina XYZ",
  "custo": 200.00,
  "observacoes": "Óleo sintético 5W30 + filtros"
}
```

**Response: 200 OK**

```json
{
  "id": 1,
  "veiculo_id": 1,
  "data_manutencao": "2024-11-15",
  "km_manutencao": 45000,
  "tipo_manutencao": "Troca de óleo e filtros",
  "prestador_servico": "Oficina XYZ",
  "custo": 200.00,
  "observacoes": "Óleo sintético 5W30 + filtros",
  "created_at": "2024-11-15T14:20:00"
}
```

---

### 5. Deletar Manutenção

Remove uma manutenção do sistema.

```http
DELETE /manutencoes/{manutencao_id}
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "message": "Manutenção deletada com sucesso",
  "id": 1
}
```

---

## 👤 Endpoints de Usuários

### 1. Listar Todos os Usuários (Admin)

```http
GET /usuarios/
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "plano_id": 1,
    "created_at": "2024-11-19T10:30:00"
  }
]
```

---

### 2. Buscar Usuário por ID

```http
GET /usuarios/{usuario_id}
```

**Headers:**

```
Authorization: Bearer {token}
```

**Response: 200 OK**

```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "plano_id": 1,
  "created_at": "2024-11-19T10:30:00",
  "veiculos": [
    {
      "id": 1,
      "placa": "ABC1234",
      "marca": "Ford",
      "modelo": "Fiesta"
    }
  ]
}
```

---

## 📋 Endpoints de Planos

### 1. Listar Planos Disponíveis

```http
GET /planos/
```

**Response: 200 OK**

```json
[
  {
    "id": 1,
    "nome": "Básico",
    "descricao": "Plano gratuito com funcionalidades básicas",
    "preco": 0.00,
    "max_veiculos": 3
  },
  {
    "id": 2,
    "nome": "Premium",
    "descricao": "Plano completo sem limites",
    "preco": 29.90,
    "max_veiculos": null
  }
]
```

---

## 📊 Modelos de Dados

### Usuario

```json
{
  "id": 1,
  "nome": "string",
  "email": "string (unique)",
  "senha": "string (hashed)",
  "plano_id": 1,
  "created_at": "datetime"
}
```

### Veiculo

```json
{
  "id": 1,
  "placa": "string (unique)",
  "marca": "string",
  "modelo": "string",
  "ano": "integer",
  "km_atual": "integer",
  "usuario_id": 1,
  "created_at": "datetime"
}
```

### Manutencao

```json
{
  "id": 1,
  "veiculo_id": 1,
  "data_manutencao": "date",
  "km_manutencao": "integer",
  "tipo_manutencao": "string",
  "prestador_servico": "string",
  "custo": "decimal(10,2)",
  "observacoes": "text (optional)",
  "created_at": "datetime"
}
```

### Plano

```json
{
  "id": 1,
  "nome": "string",
  "descricao": "text",
  "preco": "decimal(10,2)",
  "max_veiculos": "integer (nullable)"
}
```

---

## 🚦 Códigos de Status

| Código | Significado | Descrição |
|--------|-------------|-----------|
| `200` | OK | Requisição bem-sucedida |
| `201` | Created | Recurso criado com sucesso |
| `204` | No Content | Requisição bem-sucedida sem conteúdo |
| `400` | Bad Request | Dados inválidos ou regra de negócio violada |
| `401` | Unauthorized | Não autenticado ou token inválido |
| `403` | Forbidden | Sem permissão para acessar o recurso |
| `404` | Not Found | Recurso não encontrado |
| `422` | Unprocessable Entity | Erro de validação de dados |
| `500` | Internal Server Error | Erro interno do servidor |

---

## 💡 Exemplos de Uso

### Exemplo Completo: Cadastrar Veículo e Manutenção

#### 1. Fazer Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao@email.com&password=senha123"
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 2. Cadastrar Veículo

```bash
curl -X POST http://localhost:8000/veiculos/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC1234",
    "marca": "Ford",
    "modelo": "Fiesta",
    "ano": 2020,
    "km_atual": 45000
  }'
```

**Response:**

```json
{
  "id": 1,
  "placa": "ABC1234",
  "marca": "Ford",
  "modelo": "Fiesta",
  "ano": 2020,
  "km_atual": 45000,
  "usuario_id": 1
}
```

#### 3. Registrar Manutenção

```bash
curl -X POST http://localhost:8000/manutencoes/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "veiculo_id": 1,
    "data_manutencao": "2024-11-15",
    "km_manutencao": 45000,
    "tipo_manutencao": "Troca de óleo",
    "prestador_servico": "Oficina XYZ",
    "custo": 150.00
  }'
```

#### 4. Listar Manutenções do Veículo

```bash
curl -X GET "http://localhost:8000/manutencoes/?placa=ABC1234" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### Exemplo em JavaScript (Fetch API)

```javascript
// Login
async function login() {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: 'joao@email.com',
      password: 'senha123'
    })
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data.access_token;
}

// Listar Veículos
async function listarVeiculos() {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/veiculos/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
}

// Cadastrar Veículo
async function cadastrarVeiculo(veiculo) {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/veiculos/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(veiculo)
  });
  
  return await response.json();
}
```

---

### Exemplo em Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
def login(email, senha):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": email, "password": senha}
    )
    return response.json()["access_token"]

# Listar Veículos
def listar_veiculos(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/veiculos/", headers=headers)
    return response.json()

# Cadastrar Veículo
def cadastrar_veiculo(token, veiculo):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/veiculos/",
        headers=headers,
        json=veiculo
    )
    return response.json()

# Uso
token = login("joao@email.com", "senha123")
veiculos = listar_veiculos(token)
print(veiculos)
```

---

## ⚠️ Tratamento de Erros

### Formato Padrão de Erro

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Exemplos de Erros

#### 400 Bad Request

```json
{
  "detail": "Placa já cadastrada no sistema"
}
```

#### 401 Unauthorized

```json
{
  "detail": "Credenciais inválidas"
}
```

#### 404 Not Found

```json
{
  "detail": "Veículo não encontrado"
}
```

#### 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "placa"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🔒 Segurança

### Boas Práticas

- ✅ Sempre use HTTPS em produção
- ✅ Nunca exponha o SECRET_KEY
- ✅ Tokens expiram em 30 minutos
- ✅ Senhas são hasheadas com bcrypt
- ✅ Cookies são httpOnly (não acessíveis via JavaScript)
- ✅ Validação de entrada em todos os endpoints

### CORS

Configure CORS adequadamente em produção no arquivo `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Recursos Adicionais

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Repositório:** https://github.com/GuilhemeMiranda/Python_Projetos
- **Issues:** https://github.com/GuilhemeMiranda/Python_Projetos/issues

---

**Documentação mantida por [Guilherme Miranda](https://github.com/GuilhemeMiranda)**

**Última atualização:** Novembro 2024 - Versão 1.3.0