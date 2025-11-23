# 🚗 API de Manutenção Veicular

Sistema completo para gerenciamento e controle de manutenção de veículos, desenvolvido com FastAPI e SQLAlchemy.

## 📋 Sobre o Projeto

Este projeto é uma API RESTful que permite gerenciar:
- **Usuários**: Cadastro e autenticação de proprietários de veículos
- **Veículos**: Registro e acompanhamento de veículos
- **Manutenções**: Histórico completo de manutenções realizadas
- **Planos de Manutenção**: Planejamento de manutenções preventivas
- **Documentos**: Anexação de notas fiscais e comprovantes

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy**: ORM para manipulação do banco de dados
- **SQLite**: Banco de dados (pode ser substituído por PostgreSQL/MySQL)
- **Pydantic**: Validação de dados e schemas
- **Uvicorn**: Servidor ASGI para execução da aplicação

## 📁 Estrutura do Projeto

```
Python_Projetos/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── database.py          # Configuração do banco de dados
│   ├── models.py            # Modelos SQLAlchemy (tabelas)
│   ├── schemas.py           # Schemas Pydantic (validação)
│   ├── crud.py              # Operações CRUD no banco
│   └── routes/              # Rotas da API
│       ├── __init__.py
│       ├── usuarios.py      # Endpoints de usuários
│       ├── veiculos.py      # Endpoints de veículos
│       ├── manutencoes.py   # Endpoints de manutenções
│       └── planos.py        # Endpoints de planos
├── tests/                   # Testes automatizados (recomendado)
├── .gitignore              # Arquivos ignorados pelo Git
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
└── LICENSE                # Licença do projeto
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git
cd Python_Projetos
```

### Passo 2: Criar Ambiente Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Executar a Aplicação

```bash
# Modo desenvolvimento
uvicorn app.main:app --reload

# Modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📖 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI (Interativo)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Endpoints Principais

### Usuários
- `POST /usuarios/` - Criar novo usuário
- `GET /usuarios/` - Listar todos os usuários
- `GET /usuarios/buscar?email=` - Buscar usuário por email

### Veículos
- `POST /veiculos/` - Cadastrar novo veículo
- `GET /veiculos/` - Listar todos os veículos
- `GET /veiculos/{id}` - Buscar veículo por ID
- `PUT /veiculos/{id}` - Atualizar dados do veículo
- `DELETE /veiculos/{id}` - Excluir veículo

### Manutenções
- `POST /manutencoes/` - Registrar nova manutenção
- `GET /manutencoes/` - Listar todas as manutenções
- `GET /manutencoes/{id}` - Buscar manutenção por ID
- `DELETE /manutencoes/{id}` - Excluir manutenção

### Planos de Manutenção
- `POST /planos/` - Criar plano de manutenção
- `GET /planos/` - Listar todos os planos
- `GET /planos/veiculo/{id}` - Listar planos de um veículo
- `DELETE /planos/{id}` - Excluir plano

## 📝 Exemplos de Uso

### Criar um Usuário

```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "senha": "senha123"
  }'
```

### Cadastrar um Veículo

```bash
curl -X POST "http://localhost:8000/veiculos/" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "modelo": "Civic",
    "marca": "Honda",
    "ano": 2020,
    "km_atual": 15000,
    "usuario_id": 1
  }'
```

### Registrar uma Manutenção

```bash
curl -X POST "http://localhost:8000/manutencoes/" \
  -H "Content-Type: application/json" \
  -d '{
    "veiculo_id": 1,
    "data": "2024-01-15",
    "km": 15000,
    "tipo_manutencao": "Troca de óleo",
    "descricao": "Troca de óleo e filtro",
    "custo": 150.00,
    "prestador_servico": "AutoCenter Silva"
  }'
```

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-cov httpx

# Executar testes
pytest

# Executar testes com cobertura
pytest --cov=app tests/
```

## 🔄 Controle de Versão

### Branches

- `main`: Versão estável de produção
- `develop`: Branch de desenvolvimento
- `feature/*`: Novas funcionalidades
- `bugfix/*`: Correções de bugs
- `hotfix/*`: Correções urgentes

### Commits

Siga o padrão de commits semânticos:

```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: formatação de código
refactor: refatoração de código
test: adiciona ou atualiza testes
chore: tarefas de manutenção
```

### Tags e Releases

```bash
# Criar uma tag
git tag -a v1.0.0 -m "Release 1.0.0"

# Enviar tags para o repositório
git push origin --tags
```

## 🛡️ Segurança

⚠️ **Importante**: Este projeto está em desenvolvimento. Para produção:

1. **Nunca armazene senhas em texto puro**
   - Implemente hash de senhas com `bcrypt` ou `passlib`
   
2. **Use variáveis de ambiente**
   - Configure segredos através de `.env` (nunca commite este arquivo)
   
3. **Adicione autenticação JWT**
   - Proteja endpoints com tokens de autenticação
   
4. **Valide entradas**
   - Sempre valide e sanitize dados de entrada

5. **Configure CORS adequadamente**
   - Restrinja origens permitidas em produção

## 🤝 Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

Leia [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Guilherme Miranda**

- GitHub: [@GuilhemeMiranda](https://github.com/GuilhemeMiranda)

## 🔮 Roadmap

### Versão 1.1
- [ ] Autenticação JWT
- [ ] Hash de senhas
- [ ] Upload de documentos/imagens
- [ ] Filtros avançados nas listagens
- [ ] Paginação

### Versão 2.0
- [ ] Notificações de manutenção preventiva
- [ ] Dashboard com gráficos
- [ ] Exportação de relatórios (PDF)
- [ ] API de terceiros (preços de peças)
- [ ] Aplicativo mobile

## 📞 Suporte

Para reportar bugs ou sugerir melhorias:
- Abra uma [Issue](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- Entre em contato através do GitHub

## 🙏 Agradecimentos

- FastAPI pela excelente documentação
- Comunidade Python pelo suporte
- Todos os contribuidores do projeto

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
