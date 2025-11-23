# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Em Desenvolvimento
- Sistema de autenticação JWT
- Upload de documentos/imagens
- Notificações de manutenção preventiva

## [1.0.0] - 2024-11-23

### Adicionado
- Documentação completa do projeto (README.md)
- Guia de contribuição (CONTRIBUTING.md)
- Arquivo de licença MIT (LICENSE)
- Arquivo de dependências (requirements.txt)
- Changelog para rastreamento de versões
- Template de variáveis de ambiente (.env.example)
- Configuração para ferramentas de qualidade de código
- Estrutura de testes com pytest
- GitHub Actions para CI/CD
- Docker Compose para ambiente de desenvolvimento
- Makefile com comandos comuns

### Funcionalidades Principais
- **CRUD de Usuários**: Criar, listar e buscar usuários
- **CRUD de Veículos**: Operações completas para gerenciar veículos
- **CRUD de Manutenções**: Registrar e consultar histórico de manutenções
- **CRUD de Planos**: Gerenciar planos de manutenção preventiva
- **API RESTful**: Endpoints bem documentados com FastAPI
- **Banco de Dados**: Persistência com SQLite e SQLAlchemy
- **Validação**: Schemas Pydantic para validação de dados
- **Documentação Interativa**: Swagger UI e ReDoc automáticos

### Modelos de Dados
- Usuario: Gestão de usuários do sistema
- Veiculo: Cadastro de veículos com relacionamento aos usuários
- Manutencao: Histórico de manutenções realizadas
- Documento: Anexos relacionados às manutenções
- PlanoManutencao: Planejamento de manutenções preventivas

### Estrutura do Projeto
```
Python_Projetos/
├── app/
│   ├── main.py          # Ponto de entrada
│   ├── database.py      # Configuração do banco
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Schemas Pydantic
│   ├── crud.py          # Operações CRUD
│   └── routes/          # Endpoints da API
├── tests/               # Testes automatizados
├── .github/             # GitHub Actions
└── docs/               # Documentação adicional
```

## [0.2.0] - 2024-11-20

### Adicionado
- Planejamento inicial do projeto
- Estrutura básica de diretórios
- Configuração inicial do Git

## [0.1.0] - 2024-11-15

### Adicionado
- Versão inicial do projeto
- Configuração básica do FastAPI
- Modelos iniciais do banco de dados
- Primeiros endpoints de teste

---

## Tipos de Mudanças

- **Adicionado**: Novas funcionalidades
- **Alterado**: Mudanças em funcionalidades existentes
- **Descontinuado**: Funcionalidades que serão removidas
- **Removido**: Funcionalidades removidas
- **Corrigido**: Correções de bugs
- **Segurança**: Correções de vulnerabilidades

## Links de Comparação

- [Não Lançado](https://github.com/GuilhemeMiranda/Python_Projetos/compare/v1.0.0...HEAD)
- [1.0.0](https://github.com/GuilhemeMiranda/Python_Projetos/releases/tag/v1.0.0)
