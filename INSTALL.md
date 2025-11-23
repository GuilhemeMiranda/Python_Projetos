# 📥 Guia de Instalação - Sistema de Manutenção Veicular

Guia completo e detalhado para instalar e configurar o Sistema de Manutenção Veicular em qualquer ambiente.

---

## 📋 Índice

1. [Requisitos do Sistema](#-requisitos-do-sistema)
2. [Instalação do Python](#-instalação-do-python)
3. [Instalação do PostgreSQL](#-instalação-do-postgresql)
4. [Clonando o Projeto](#-clonando-o-projeto)
5. [Configurando o Ambiente](#-configurando-o-ambiente)
6. [Configurando o Banco de Dados](#-configurando-o-banco-de-dados)
7. [Instalando Dependências](#-instalando-dependências)
8. [Configurando Variáveis de Ambiente](#-configurando-variáveis-de-ambiente)
9. [Inicializando o Sistema](#-inicializando-o-sistema)
10. [Verificação da Instalação](#-verificação-da-instalação)
11. [Problemas Comuns](#-problemas-comuns)
12. [Próximos Passos](#-próximos-passos)

---

## 💻 Requisitos do Sistema

### Hardware Mínimo

| Componente | Requisito |
|------------|-----------|
| **Processador** | Dual-core 2.0 GHz |
| **RAM** | 4 GB |
| **Espaço em Disco** | 500 MB livres |
| **Conexão Internet** | Necessária para instalação |

### Software Obrigatório

- ✅ Python 3.9 ou superior
- ✅ PostgreSQL 13 ou superior
- ✅ pip (gerenciador de pacotes Python)

### Software Opcional

- 📦 Git (para clonar o repositório)
- 🔧 pgAdmin 4 (interface gráfica para PostgreSQL)
- 📝 VS Code (editor de código recomendado)

### Sistemas Operacionais Suportados

- ✅ Windows 10/11
- ✅ Ubuntu 20.04+ / Debian 10+
- ✅ macOS 10.15+

---

## 🐍 Instalação do Python

### Windows

#### Passo 1: Baixar o Instalador

1. Acesse: https://www.python.org/downloads/
2. Clique em **"Download Python 3.x.x"** (versão mais recente)
3. Execute o arquivo baixado

#### Passo 2: Instalar

1. ⚠️ **IMPORTANTE:** Marque a opção **"Add Python to PATH"**
2. Clique em **"Install Now"**
3. Aguarde a instalação concluir
4. Clique em **"Close"**

#### Passo 3: Verificar Instalação

Abra o PowerShell ou CMD e execute:

```powershell
python --version
# Deve mostrar: Python 3.x.x

pip --version
# Deve mostrar: pip x.x.x
```

---

### Linux (Ubuntu/Debian)

```bash
# Atualizar repositórios
sudo apt update

# Instalar Python 3.9+
sudo apt install python3.9 python3.9-venv python3-pip

# Verificar instalação
python3 --version
pip3 --version
```

---

### macOS

#### Opção 1: Homebrew (Recomendado)

```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.9

# Verificar instalação
python3 --version
pip3 --version
```

#### Opção 2: Download Direto

1. Acesse: https://www.python.org/downloads/mac-osx/
2. Baixe o instalador
3. Execute e siga as instruções

---

## 🐘 Instalação do PostgreSQL

### Windows

#### Passo 1: Baixar o Instalador

1. Acesse: https://www.postgresql.org/download/windows/
2. Clique em **"Download the installer"**
3. Selecione a versão mais recente (13+)
4. Execute o instalador

#### Passo 2: Instalar

1. Clique em **"Next"** nas telas iniciais
2. **Diretório de Instalação:** Deixe o padrão
3. **Componentes:** Marque todos (PostgreSQL Server, pgAdmin 4, Stack Builder, Command Line Tools)
4. **Diretório de Dados:** Deixe o padrão
5. **Senha do Superusuário:**
   - Digite uma senha forte
   - ⚠️ **ANOTE ESSA SENHA!** Você vai precisar dela
6. **Porta:** Deixe `5432` (padrão)
7. **Locale:** Deixe o padrão
8. Clique em **"Next"** e depois **"Install"**
9. Desmarque **"Stack Builder"** no final
10. Clique em **"Finish"**

#### Passo 3: Verificar Instalação

Abra o PowerShell:

```powershell
psql --version
# Deve mostrar: psql (PostgreSQL) 13.x
```

Se não funcionar, adicione ao PATH:
- Painel de Controle → Sistema → Configurações Avançadas
- Variáveis de Ambiente → Path → Editar
- Adicione: `C:\Program Files\PostgreSQL\13\bin`

---

### Linux (Ubuntu/Debian)

```bash
# Atualizar repositórios
sudo apt update

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Iniciar o serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar status
sudo systemctl status postgresql

# Configurar senha do postgres
sudo -u postgres psql
postgres=# \password postgres
# Digite a senha
postgres=# \q
```

---

### macOS

```bash
# Instalar com Homebrew
brew install postgresql

# Iniciar o serviço
brew services start postgresql

# Criar usuário postgres (se necessário)
createuser -s postgres

# Configurar senha
psql postgres
postgres=# \password postgres
# Digite a senha
postgres=# \q
```

---

## 📦 Clonando o Projeto

### Opção 1: Com Git (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git

# Entre na pasta do projeto
cd Python_Projetos/Manutencao_Veicular

# Verifique os arquivos
ls  # Linux/Mac
dir # Windows
```

### Opção 2: Download ZIP

1. Acesse: https://github.com/GuilhemeMiranda/Python_Projetos
2. Clique em **"Code"** → **"Download ZIP"**
3. Extraia o arquivo ZIP
4. Entre na pasta `Manutencao_Veicular`

---

## 🔧 Configurando o Ambiente

### Criar Ambiente Virtual

**Windows:**

```powershell
# Entre na pasta do projeto
cd Manutencao_Veicular

# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente
.venv\Scripts\activate

# Você verá (.venv) no início do prompt
```

**Linux/macOS:**

```bash
# Entre na pasta do projeto
cd Manutencao_Veicular

# Crie o ambiente virtual
python3 -m venv .venv

# Ative o ambiente
source .venv/bin/activate

# Você verá (.venv) no início do prompt
```

### Por que usar Ambiente Virtual?

- ✅ Isola as dependências do projeto
- ✅ Evita conflitos com outros projetos Python
- ✅ Facilita o gerenciamento de versões
- ✅ Permite diferentes versões de pacotes por projeto

---

## 🗄️ Configurando o Banco de Dados

### Criar o Banco de Dados

#### Método 1: Linha de Comando

**Windows:**

```powershell
# Acesse o PostgreSQL (digite a senha quando solicitado)
psql -U postgres

# Crie o banco
CREATE DATABASE manutencao_veicular;

# Verifique se foi criado
\l

# Saia
\q
```

**Linux/macOS:**

```bash
# Acesse o PostgreSQL
sudo -u postgres psql

# Crie o banco
CREATE DATABASE manutencao_veicular;

# Verifique
\l

# Saia
\q
```

#### Método 2: pgAdmin 4 (Interface Gráfica)

1. Abra o **pgAdmin 4**
2. Clique com botão direito em **Databases**
3. Selecione **Create** → **Database**
4. **Database:** `manutencao_veicular`
5. **Owner:** `postgres`
6. Clique em **Save**

### Verificar Conexão

```bash
# Teste a conexão
psql -U postgres -d manutencao_veicular

# Se conectar com sucesso, está tudo OK!
\q
```

---

## 📚 Instalando Dependências

### Atualizar pip

```bash
# Atualize o pip
python -m pip install --upgrade pip
```

### Instalar Dependências do Projeto

```bash
# Instale todas as dependências
pip install -r requirements.txt
```

### Pacotes Instalados

O arquivo `requirements.txt` contém:

```txt
# Framework Web
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Banco de Dados
sqlalchemy==2.0.25
psycopg2-binary==2.9.9

# Autenticação
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2

# Templates
jinja2==3.1.3

# Requisições HTTP
requests==2.31.0
httpx==0.26.0

# Configuração
python-dotenv==1.0.0

# Validação
pydantic==2.5.3
pydantic-settings==2.1.0
email-validator==2.1.0

# Utilitários
python-dateutil==2.8.2
```

### Verificar Instalação

```bash
# Liste os pacotes instalados
pip list

# Deve mostrar todos os pacotes acima
```

---

## ⚙️ Configurando Variáveis de Ambiente

### Criar arquivo .env

**Windows:**

```powershell
# Copie o arquivo de exemplo
copy .env.example .env
```

**Linux/macOS:**

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

### Editar o arquivo .env

Abra o arquivo `.env` com seu editor preferido e configure:

```env
# ====================================
# DATABASE CONFIGURATION
# ====================================
DATABASE_URL=postgresql://postgres:SUA_SENHA_AQUI@localhost:5432/manutencao_veicular

# ====================================
# JWT CONFIGURATION
# ====================================
SECRET_KEY=GERE_UMA_CHAVE_AQUI
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ====================================
# APPLICATION SETTINGS
# ====================================
APP_NAME=Sistema de Manutenção Veicular
APP_VERSION=1.3.0
DEBUG=True

# ====================================
# SERVER CONFIGURATION
# ====================================
HOST=0.0.0.0
PORT=8000
```

### Gerar SECRET_KEY

Execute um dos comandos:

**Opção 1: Python**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Opção 2: OpenSSL**

```bash
openssl rand -hex 32
```

Copie a chave gerada e cole no `.env`:

```env
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

### Configurar DATABASE_URL

Substitua `SUA_SENHA_AQUI` pela senha do PostgreSQL:

```env
DATABASE_URL=postgresql://postgres:minha_senha_123@localhost:5432/manutencao_veicular
```

### ⚠️ Segurança

- ❌ **NUNCA** commite o arquivo `.env` no Git
- ✅ O `.gitignore` já está configurado para ignorá-lo
- ✅ Use senhas fortes
- ✅ Troque a SECRET_KEY em produção

---

## 🚀 Inicializando o Sistema

### Método 1: Script Automatizado (Windows)

```powershell
# Execute o script
start.bat
```

O script faz:
1. Ativa o ambiente virtual
2. Verifica conexão com banco
3. Inicia o servidor Uvicorn

---

### Método 2: Manual

**Ative o ambiente virtual primeiro!**

**Windows:**

```powershell
# Ative o ambiente
.venv\Scripts\activate

# Inicie o servidor
python -m uvicorn app.main:app --reload --port 8000
```

**Linux/macOS:**

```bash
# Ative o ambiente
source .venv/bin/activate

# Inicie o servidor
uvicorn app.main:app --reload --port 8000
```

### Saída Esperada

```
INFO:     Will watch for changes in these directories: ['C:\\...\\Manutencao_Veicular']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### O que significa `--reload`?

- 🔄 Reinicia automaticamente quando você altera o código
- 💡 Útil para desenvolvimento
- ❌ Não use em produção

---

## ✅ Verificação da Instalação

### 1. Testar o Servidor

Abra o navegador e acesse:

#### Interface Principal
- **Login:** http://localhost:8000/ui/login
- **Registro:** http://localhost:8000/ui/registro
- **Dashboard:** http://localhost:8000/ui/ (após login)

#### Documentação da API
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 2. Verificar Banco de Dados

```sql
-- Acesse o PostgreSQL
psql -U postgres -d manutencao_veicular

-- Liste as tabelas (após primeira execução)
\dt

-- Você deve ver:
-- public | manutencoes | table | postgres
-- public | planos      | table | postgres
-- public | usuarios    | table | postgres
-- public | veiculos    | table | postgres

-- Saia
\q
```

### 3. Criar Primeiro Usuário

1. Acesse: http://localhost:8000/ui/registro
2. Preencha o formulário:
   - **Nome:** Seu Nome
   - **Email:** seu@email.com
   - **Senha:** suasenha123
   - **Confirmar Senha:** suasenha123
3. Clique em **"Cadastrar"**
4. Você deve ver: "Usuário cadastrado com sucesso!"

### 4. Fazer Login

1. Acesse: http://localhost:8000/ui/login
2. Digite suas credenciais
3. Clique em **"Entrar"**
4. Você será redirecionado para o Dashboard

### 5. Testar Scripts Utilitários

```bash
# Liste usuários cadastrados
python scripts/list_users.py

# Debug de autenticação
python scripts/debug_auth.py

# Verificar login local
python scripts/check_login_local.py
```

---

## 🔧 Problemas Comuns

### 1. "ModuleNotFoundError: No module named 'fastapi'"

**Causa:** Ambiente virtual não está ativado ou dependências não foram instaladas.

**Solução:**

```bash
# Ative o ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Você DEVE ver (.venv) no prompt

# Reinstale as dependências
pip install -r requirements.txt
```

---

### 2. "could not connect to server: Connection refused"

**Causa:** PostgreSQL não está rodando.

**Solução:**

**Windows:**

```powershell
# Inicie o serviço
net start postgresql-x64-13
```

**Linux:**

```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

**macOS:**

```bash
brew services start postgresql
```

---

### 3. "FATAL: password authentication failed for user 'postgres'"

**Causa:** Senha incorreta no arquivo `.env`.

**Solução:**

1. Verifique a senha no `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:SUA_SENHA_AQUI@localhost:5432/manutencao_veicular
   ```

2. Ou redefina a senha do PostgreSQL:
   ```bash
   psql -U postgres
   \password postgres
   # Digite a nova senha
   \q
   ```

3. Atualize o `.env` com a nova senha

---

### 4. "Port 8000 is already in use"

**Causa:** Outra aplicação está usando a porta 8000.

**Soluções:**

**Opção 1: Use outra porta**

```bash
uvicorn app.main:app --reload --port 8001
```

**Opção 2: Mate o processo na porta 8000**

**Windows:**

```powershell
# Encontre o processo
netstat -ano | findstr :8000

# Mate o processo (substitua PID)
taskkill /PID 12345 /F
```

**Linux/macOS:**

```bash
# Encontre e mate o processo
lsof -ti:8000 | xargs kill -9
```

---

### 5. "database 'manutencao_veicular' does not exist"

**Causa:** Banco de dados não foi criado.

**Solução:**

```sql
psql -U postgres
CREATE DATABASE manutencao_veicular;
\l
\q
```

---

### 6. "ImportError: cannot import name 'app' from 'app.main'"

**Causa:** Você está na pasta errada.

**Solução:**

```bash
# Certifique-se de estar em Manutencao_Veicular/
pwd  # Linux/Mac
cd  # Windows

# Verifique se o arquivo existe
ls app/main.py  # Linux/Mac
dir app\main.py  # Windows
```

---

### 7. "pip: command not found"

**Causa:** Python não foi adicionado ao PATH.

**Solução:**

**Windows:**
- Reinstale o Python marcando "Add Python to PATH"

**Linux/macOS:**
```bash
# Use pip3
pip3 install -r requirements.txt
```

---

### 8. Erro ao instalar psycopg2

**Windows:**

Se aparecer erro ao instalar `psycopg2`, use:

```bash
pip install psycopg2-binary
```

**Linux:**

```bash
# Instale dependências
sudo apt install libpq-dev python3-dev

# Reinstale
pip install psycopg2-binary
```

---

### 9. "Access is denied" ao ativar ambiente virtual

**Windows:**

```powershell
# Execute como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Tente novamente
.venv\Scripts\activate
```

---

### 10. Tabelas não são criadas automaticamente

**Solução:**

As tabelas são criadas na primeira execução. Se não forem:

```python
# Execute no Python
python

>>> from app.database import engine, Base
>>> from app.models import Usuario, Veiculo, Manutencao, Plano
>>> Base.metadata.create_all(bind=engine)
>>> exit()
```

---

## 🎯 Próximos Passos

Após a instalação bem-sucedida:

### 1. Explore o Sistema

- ✅ Acesse o Dashboard
- ✅ Cadastre um veículo de teste
- ✅ Registre uma manutenção
- ✅ Veja os relatórios

### 2. Leia a Documentação

- 📖 [Manual do Usuário](docs/MANUAL_USUARIO.md)
- 🔌 [Documentação da API](docs/API.md)
- 🤝 [Guia de Contribuição](docs/CONTRIBUTING.md)

### 3. Personalize

- 🎨 Ajuste cores em `app/static/styles.css`
- ⚙️ Configure variáveis no `.env`
- 📝 Adapte templates em `app/templates/`

### 4. Desenvolva

- 💻 Crie novas features
- 🧪 Adicione testes
- 📚 Melhore a documentação

---

## 📞 Precisa de Ajuda?

### Recursos

- 📖 [README.md](README.md) - Visão geral do projeto
- 📚 [Manual do Usuário](docs/MANUAL_USUARIO.md)
- 🔌 [API Docs](docs/API.md)
- 🐛 [Reportar Bug](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- 💬 [Discussões](https://github.com/GuilhemeMiranda/Python_Projetos/discussions)

### Contato

- GitHub: [@GuilhemeMiranda](https://github.com/GuilhemeMiranda)
- Email: contato@exemplo.com

---

## 📝 Checklist de Instalação

Use este checklist para garantir que tudo foi configurado:

- [ ] Python 3.9+ instalado
- [ ] PostgreSQL 13+ instalado
- [ ] Projeto clonado/baixado
- [ ] Ambiente virtual criado
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Arquivo `.env` configurado
- [ ] SECRET_KEY gerada
- [ ] DATABASE_URL configurada
- [ ] Servidor iniciado com sucesso
- [ ] Interface acessível no navegador
- [ ] Primeiro usuário criado
- [ ] Login realizado com sucesso
- [ ] Dashboard funcionando

---

**Instalação concluída com sucesso! 🎉**

**Desenvolvido com ❤️ por [Guilherme Miranda](https://github.com/GuilhemeMiranda)**