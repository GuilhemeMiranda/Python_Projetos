# 🚗 Sistema de Manutenção Veicular

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-1.3.0-orange.svg)

**Sistema web completo para gerenciamento de veículos e suas manutenções**

[Instalação](#-instalação) • 
[Como Usar](#-como-usar) • 
[Documentação](#-documentação) • 
[API](#-api-endpoints) • 
[Contribuir](#-contribuindo)

![Dashboard Preview](https://via.placeholder.com/800x400/007bff/ffffff?text=Dashboard+Preview)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Documentação](#-documentação)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

O **Sistema de Manutenção Veicular** é uma aplicação web moderna desenvolvida com FastAPI e PostgreSQL para facilitar o controle e acompanhamento de veículos e suas manutenções. 

Com uma interface intuitiva e responsiva, permite que você:
- 📊 Mantenha um histórico completo de manutenções
- 💰 Controle custos e despesas
- 📈 Visualize estatísticas em tempo real
- 🔍 Filtre e busque informações rapidamente

### ✨ Principais Destaques

- 🔐 **Autenticação Segura** - Sistema JWT com cookies httpOnly
- 📊 **Dashboard Interativo** - Estatísticas em tempo real dos seus veículos
- 🚗 **Gestão de Veículos** - CRUD completo com validações
- 🔧 **Controle de Manutenções** - Histórico detalhado e editável
- 📱 **Design Responsivo** - Funciona perfeitamente em desktop, tablet e mobile
- 🎨 **Interface Moderna** - UI/UX pensada para produtividade
- 🔍 **Filtros Avançados** - Busque por placa, período ou tipo
- 💾 **Banco Robusto** - PostgreSQL com SQLAlchemy ORM
- 📝 **Validações Inteligentes** - Pydantic schemas garantem integridade

---

## 🚀 Funcionalidades

### 👤 Gerenciamento de Usuários
- ✅ Cadastro de novos usuários com validação de email
- ✅ Login seguro com JWT tokens
- ✅ Logout com limpeza de sessão
- ✅ Perfis de usuário com diferentes planos
- ✅ Autenticação obrigatória em rotas protegidas

### 🚗 Gestão de Veículos
- ✅ Cadastrar veículos (placa, marca, modelo, ano, quilometragem)
- ✅ Listar todos os veículos do usuário logado
- ✅ Editar informações dos veículos
- ✅ Excluir veículos com confirmação
- ✅ Filtrar veículos por placa
- ✅ Validação de placa única no sistema
- ✅ Controle de quilometragem atual
- ✅ Modal de edição inline

### 🔧 Registro de Manutenções
- ✅ Registrar manutenções por veículo
- ✅ Informações completas: data, km, tipo, prestador, custo
- ✅ Campo de observações opcionais
- ✅ Editar manutenções existentes
- ✅ Excluir manutenções com confirmação
- ✅ Filtrar manutenções por veículo
- ✅ Validação de quilometragem progressiva
- ✅ Formatação automática de valores monetários

### 📊 Dashboard e Relatórios
- ✅ Total de veículos cadastrados
- ✅ Quantidade de manutenções registradas
- ✅ Custo total formatado em reais (R$)
- ✅ Cards de acesso rápido às funcionalidades
- ✅ Tabelas responsivas com ações inline
- ✅ Modais elegantes para edição/exclusão
- ✅ Atualização em tempo real

### 🎨 Interface do Usuário
- ✅ Menu lateral responsivo com ícones
- ✅ Design moderno com fonte Barlow
- ✅ Modais elegantes para ações
- ✅ Mensagens de feedback (sucesso/erro)
- ✅ Animações suaves e transições
- ✅ Mobile-first responsivo
- ✅ Temas consistentes em todas as páginas

---

## 🛠 Tecnologias

### Backend
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **[Python](https://www.python.org/)** | 3.9+ | Linguagem de programação |
| **[FastAPI](https://fastapi.tiangolo.com/)** | 0.109.0 | Framework web moderno e rápido |
| **[SQLAlchemy](https://www.sqlalchemy.org/)** | 2.0.25 | ORM para banco de dados |
| **[PostgreSQL](https://www.postgresql.org/)** | 13+ | Banco de dados relacional |
| **[Pydantic](https://pydantic-docs.helpmanual.io/)** | 2.5.3 | Validação de dados |
| **[Python-Jose](https://python-jose.readthedocs.io/)** | 3.3.0 | JWT tokens |
| **[Passlib](https://passlib.readthedocs.io/)** | 1.7.4 | Hash de senhas com bcrypt |
| **[Uvicorn](https://www.uvicorn.org/)** | 0.27.0 | Servidor ASGI |

### Frontend
| Tecnologia | Descrição |
|------------|-----------|
| **HTML5** | Estrutura semântica |
| **CSS3** | Estilos modernos com variáveis CSS |
| **JavaScript ES6+** | Interatividade e requisições assíncronas |
| **[Jinja2](https://jinja.palletsprojects.com/)** | Template engine |
| **Fetch API** | Requisições HTTP assíncronas |
| **Barlow Font** | Tipografia moderna do Google Fonts |

### Ferramentas de Desenvolvimento
- **Git** - Controle de versão
- **VS Code** - IDE recomendada
- **pgAdmin 4** - Interface gráfica para PostgreSQL
- **Postman** - Testes de API (opcional)

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### Obrigatórios
- ✅ **Python 3.9 ou superior**
  - [Download Python](https://www.python.org/downloads/)
  - Verificar: `python --version`

- ✅ **PostgreSQL 13 ou superior**
  - [Download PostgreSQL](https://www.postgresql.org/download/)
  - Verificar: `psql --version`

- ✅ **pip** (gerenciador de pacotes Python)
  - Geralmente vem com Python
  - Verificar: `pip --version`

### Opcionais
- **Git** - Para clonar o repositório
  - [Download Git](https://git-scm.com/downloads/)
  - Verificar: `git --version`

### Requisitos de Sistema
- **SO:** Windows 10+, Linux (Ubuntu 20.04+), macOS 10.15+
- **RAM:** 4 GB mínimo
- **Espaço em Disco:** 500 MB livres
- **Navegador:** Chrome, Firefox, Edge ou Safari (versões recentes)

---

## ⚙️ Instalação

### 🚀 Instalação Rápida (Windows)

```powershell
# 1. Clone o repositório
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git
cd Python_Projetos/Manutencao_Veicular

# 2. Execute o script de instalação
install.bat

# 3. Configure o arquivo .env
# Edite o arquivo .env com suas configurações

# 4. Inicie o sistema
start.bat
```

### 📖 Instalação Detalhada

Para um guia completo passo a passo, consulte **[INSTALL.md](INSTALL.md)**.

O guia inclui:
- Instalação do Python em diferentes sistemas
- Configuração do PostgreSQL
- Criação do ambiente virtual
- Instalação de dependências
- Configuração de variáveis de ambiente
- Solução de problemas comuns

---

## 🔧 Configuração

### 1. Criar Banco de Dados

```sql
-- Acesse o PostgreSQL
psql -U postgres

-- Crie o banco de dados
CREATE DATABASE manutencao_veicular;

-- Verifique
\l

-- Saia
\q
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e edite:

```bash
cp .env.example .env
```

Configure o arquivo `.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/manutencao_veicular

# JWT
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Sistema de Manutenção Veicular
APP_VERSION=1.3.0
DEBUG=True
```

### 3. Gerar SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🎮 Como Usar

### Iniciando o Sistema

**Windows (Recomendado):**
```powershell
start.bat
```

**Manual:**
```bash
# Ative o ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Inicie o servidor
uvicorn app.main:app --reload --port 8000
```

### Acessando o Sistema

1. **Abra o navegador em:** http://localhost:8000/ui/login

2. **Primeiro acesso:**
   - Clique em "Criar nova conta"
   - Preencha: Nome, Email, Senha
   - Clique em "Cadastrar"

3. **Login:**
   - Digite seu email e senha
   - Clique em "Entrar"

### Fluxo de Uso Básico

```
📝 1. Cadastrar Veículo
   └─→ Preencha: Placa, Marca, Modelo, Ano, KM
   
🔧 2. Registrar Manutenção
   └─→ Selecione veículo e preencha detalhes
   
📊 3. Visualizar Dashboard
   └─→ Veja estatísticas em tempo real
   
📋 4. Consultar Relatórios
   └─→ Filtre e visualize histórico
```

### Guias Detalhados

- 📖 **[Manual do Usuário](docs/MANUAL_USUARIO.md)** - Guia completo de uso
- 🔌 **[Documentação da API](docs/API.md)** - Referência da API REST
- 🤝 **[Guia de Contribuição](docs/CONTRIBUTING.md)** - Como contribuir

---

## 📁 Estrutura do Projeto

```
Manutencao_Veicular/
├── 📱 app/                        # Aplicação principal
│   ├── __init__.py
│   ├── main.py                    # Ponto de entrada FastAPI
│   ├── database.py                # Configuração do banco
│   ├── models.py                  # Modelos SQLAlchemy
│   ├── schemas.py                 # Schemas Pydantic
│   ├── crud.py                    # Operações CRUD
│   ├── security.py                # Autenticação JWT
│   │
│   ├── 🛣️ routes/                 # Rotas da API
│   │   ├── auth.py               # Autenticação
│   │   ├── veiculos.py           # Veículos
│   │   ├── manutencoes.py        # Manutenções
│   │   ├── usuarios.py           # Usuários
│   │   └── planos.py             # Planos
│   │
│   ├── 🎨 static/                 # Arquivos estáticos
│   │   ├── styles.css            # Estilos globais
│   │   ├── app.js                # JavaScript global
│   │   ├── auth.js               # Autenticação
│   │   ├── registro.js           # Cadastro
│   │   ├── veiculo.js            # Formulário veículo
│   │   ├── veiculo_list.js       # Lista veículos
│   │   └── manutencao_report.js  # Relatório
│   │
│   └── 📄 templates/              # Templates HTML
│       ├── base.html             # Template base
│       ├── index.html            # Dashboard
│       ├── login.html            # Login
│       ├── registro.html         # Cadastro
│       ├── veiculo_list.html     # Lista veículos
│       ├── veiculo_form.html     # Form veículo
│       ├── manutencao_form.html  # Form manutenção
│       └── manutencao_report.html # Relatório
│
├── 🔧 scripts/                    # Scripts utilitários
│   ├── list_users.py             # Listar usuários
│   ├── debug_auth.py             # Debug autenticação
│   └── check_login_local.py      # Verificar login
│
├── 📚 docs/                       # Documentação
│   ├── MANUAL_USUARIO.md         # Manual do usuário
│   ├── API.md                    # Documentação da API
│   └── CONTRIBUTING.md           # Guia de contribuição
│
├── 🧪 TESTES/                     # Testes (a implementar)
│
├── 📝 Arquivos de Configuração
├── .env                          # Variáveis de ambiente
├── .env.example                  # Exemplo de .env
├── .gitignore                    # Arquivos ignorados
├── requirements.txt              # Dependências Python
│
├── 🚀 Scripts de Automação
├── install.bat                   # Script de instalação
├── start.bat                     # Script de inicialização
│
└── 📖 Documentação
    ├── README.md                 # Este arquivo
    ├── INSTALL.md                # Guia de instalação
    ├── CHANGELOG.md              # Histórico de versões
    └── LICENSE                   # Licença MIT
```

---

## 🔌 API Endpoints

### 🔐 Autenticação

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/auth/register` | Registrar novo usuário | ❌ |
| `POST` | `/auth/login` | Login (retorna JWT) | ❌ |
| `POST` | `/auth/logout` | Logout | ✅ |
| `GET` | `/auth/me` | Dados do usuário logado | ✅ |

### 🚗 Veículos

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/veiculos/` | Listar veículos do usuário | ✅ |
| `POST` | `/veiculos/` | Criar novo veículo | ✅ |
| `GET` | `/veiculos/{id}` | Buscar veículo por ID | ✅ |
| `PUT` | `/veiculos/{id}` | Atualizar veículo | ✅ |
| `DELETE` | `/veiculos/{id}` | Deletar veículo | ✅ |

### 🔧 Manutenções

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/manutencoes/` | Listar manutenções | ✅ |
| `POST` | `/manutencoes/` | Criar manutenção | ✅ |
| `GET` | `/manutencoes/{id}` | Buscar manutenção por ID | ✅ |
| `PUT` | `/manutencoes/{id}` | Atualizar manutenção | ✅ |
| `DELETE` | `/manutencoes/{id}` | Deletar manutenção | ✅ |

### 🖥️ Interface Web (UI)

| Endpoint | Descrição |
|----------|-----------|
| `/ui/` | Dashboard principal |
| `/ui/login` | Página de login |
| `/ui/registro` | Página de cadastro |
| `/ui/veiculos` | Lista de veículos |
| `/ui/veiculo/novo` | Formulário novo veículo |
| `/ui/manutencao/nova` | Formulário nova manutenção |
| `/ui/manutencoes` | Relatório de manutenções |

### 📖 Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

**Documentação completa:** [docs/API.md](docs/API.md)

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| **[INSTALL.md](INSTALL.md)** | Guia completo de instalação |
| **[MANUAL_USUARIO.md](docs/MANUAL_USUARIO.md)** | Manual do usuário final |
| **[API.md](docs/API.md)** | Documentação da API REST |
| **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** | Guia para contribuidores |
| **[CHANGELOG.md](CHANGELOG.md)** | Histórico de versões |

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/007bff/ffffff?text=Dashboard+com+Estatisticas)

### Lista de Veículos
![Veículos](https://via.placeholder.com/800x400/28a745/ffffff?text=Lista+de+Veiculos)

### Relatório de Manutenções
![Relatório](https://via.placeholder.com/800x400/ffc107/ffffff?text=Relatorio+de+Manutencoes)

---

## 🗺️ Roadmap

### ✅ Versão 1.3.0 (Atual)
- [x] Dashboard com estatísticas
- [x] Menu lateral unificado
- [x] Modais de edição/exclusão
- [x] Filtros avançados

### 🚀 Versão 1.4.0 (Próxima)
- [ ] Exportação de relatórios em PDF
- [ ] Gráficos de custos mensais
- [ ] Notificações de manutenções próximas
- [ ] Upload de fotos dos veículos
- [ ] Histórico de alterações

### 🔮 Versão 2.0.0 (Futuro)
- [ ] App mobile (React Native)
- [ ] Lembretes por email
- [ ] Integração com agenda
- [ ] Múltiplos usuários por veículo
- [ ] Modo escuro
- [ ] Suporte a múltiplos idiomas

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! 

### Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch** para sua feature
   ```bash
   git checkout -b feature/MinhaFeature
   ```
3. **Commit suas mudanças**
   ```bash
   git commit -m 'feat: adiciona MinhaFeature'
   ```
4. **Push para a branch**
   ```bash
   git push origin feature/MinhaFeature
   ```
5. **Abra um Pull Request**

### Padrão de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação (sem mudança de código)
- `refactor:` Refatoração de código
- `test:` Adicionar testes
- `chore:` Tarefas de manutenção

### Guia Completo

Leia o [Guia de Contribuição](docs/CONTRIBUTING.md) para mais detalhes.

---

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app tests/

# Executar testes específicos
pytest tests/test_auth.py
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2024 Guilherme Miranda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software")...
```

---

## 👨‍💻 Autor

**Guilherme Miranda**

- GitHub: [@GuilhemeMiranda](https://github.com/GuilhemeMiranda)
- Projeto: [Python_Projetos](https://github.com/GuilhemeMiranda/Python_Projetos)
- Email: contato@exemplo.com

---

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework incrível e bem documentado
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM poderoso e flexível
- [PostgreSQL](https://www.postgresql.org/) - Banco de dados robusto
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validação de dados elegante
- Comunidade Python Brasil - Sempre prestativa e acolhedora

---

## 📞 Suporte

Precisa de ajuda? Entre em contato:

- 🐛 **Reportar Bug:** [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- 💡 **Sugerir Feature:** [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- 💬 **Discussões:** [Discussions](https://github.com/GuilhemeMiranda/Python_Projetos/discussions)
- 📧 **Email:** contato@exemplo.com

---

## 📊 Status do Projeto

```
🟢 Ativo e em desenvolvimento
📦 Versão atual: 1.3.0
🚀 Última atualização: Novembro 2024
⭐ Estrelas: Dê uma estrela se gostou!
```

---

## 🔗 Links Úteis

- [Repositório GitHub](https://github.com/GuilhemeMiranda/Python_Projetos)
- [Releases](https://github.com/GuilhemeMiranda/Python_Projetos/releases)
- [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- [Wiki](https://github.com/GuilhemeMiranda/Python_Projetos/wiki)

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

**Desenvolvido com ❤️ por [Guilherme Miranda](https://github.com/GuilhemeMiranda)**

[⬆ Voltar ao topo](#-sistema-de-manutenção-veicular)

</div>