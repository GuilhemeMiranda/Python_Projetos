# Contribuindo para o Projeto API de Manutenção Veicular

Obrigado por considerar contribuir para este projeto! Este documento fornece diretrizes e boas práticas para contribuir.

## 📋 Índice

1. [Código de Conduta](#código-de-conduta)
2. [Como Posso Contribuir?](#como-posso-contribuir)
3. [Fluxo de Trabalho Git](#fluxo-de-trabalho-git)
4. [Padrões de Código](#padrões-de-código)
5. [Padrões de Commit](#padrões-de-commit)
6. [Pull Requests](#pull-requests)
7. [Reportando Bugs](#reportando-bugs)
8. [Sugerindo Melhorias](#sugerindo-melhorias)

## 📜 Código de Conduta

Este projeto adota um código de conduta. Ao participar, você concorda em manter um ambiente respeitoso e inclusivo para todos.

### Nossos Padrões

- Use linguagem acolhedora e inclusiva
- Respeite pontos de vista diferentes
- Aceite críticas construtivas com elegância
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros

## 🤝 Como Posso Contribuir?

### Reportando Bugs

Encontrou um bug? Ajude-nos a melhorar:

1. Verifique se o bug já não foi reportado nas [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
2. Se não foi, crie uma nova issue incluindo:
   - Título claro e descritivo
   - Descrição detalhada do problema
   - Passos para reproduzir o bug
   - Comportamento esperado vs. comportamento atual
   - Screenshots (se aplicável)
   - Versão do Python e sistema operacional

### Sugerindo Melhorias

Tem uma ideia para melhorar o projeto?

1. Verifique se a sugestão já não existe
2. Abra uma issue com a tag `enhancement`
3. Descreva claramente:
   - O problema que a melhoria resolve
   - A solução proposta
   - Alternativas consideradas
   - Impacto esperado

### Implementando Funcionalidades

1. Escolha uma issue existente ou crie uma nova
2. Comente na issue que você vai trabalhar nela
3. Faça um fork do projeto
4. Crie uma branch para sua feature
5. Implemente suas mudanças
6. Escreva/atualize testes
7. Envie um Pull Request

## 🔀 Fluxo de Trabalho Git

### Estrutura de Branches

```
main (produção)
  └── develop (desenvolvimento)
       ├── feature/nome-da-feature
       ├── bugfix/nome-do-bug
       └── hotfix/nome-do-hotfix
```

### Tipos de Branches

- **main**: Código em produção (protegida)
- **develop**: Código em desenvolvimento
- **feature/**: Novas funcionalidades
- **bugfix/**: Correções de bugs
- **hotfix/**: Correções urgentes em produção

### Criando uma Nova Branch

```bash
# Atualizar develop
git checkout develop
git pull origin develop

# Criar nova branch
git checkout -b feature/minha-funcionalidade

# Trabalhe em suas mudanças...

# Commit suas mudanças
git add .
git commit -m "feat: adiciona minha funcionalidade"

# Push para o repositório
git push origin feature/minha-funcionalidade
```

### Mantendo sua Branch Atualizada

```bash
# Estando em sua branch
git fetch origin
git rebase origin/develop

# Se houver conflitos, resolva-os e:
git rebase --continue
```

### Comandos Git Úteis

```bash
# Ver status das mudanças
git status

# Ver diferenças
git diff

# Ver log de commits
git log --oneline --graph

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer mudanças em arquivo
git checkout -- arquivo.py

# Limpar arquivos não rastreados
git clean -fd
```

## 🎨 Padrões de Código

### Python Style Guide

Seguimos o [PEP 8](https://pep8.org/) com algumas adaptações:

```python
# ✅ BOM
def calcular_preco_total(preco_unitario: float, quantidade: int) -> float:
    """
    Calcula o preço total baseado no preço unitário e quantidade.
    
    Args:
        preco_unitario: Preço de um item
        quantidade: Número de itens
        
    Returns:
        Preço total calculado
    """
    return preco_unitario * quantidade

# ❌ EVITAR
def calc(p,q):
    return p*q
```

### Convenções de Nomenclatura

- **Classes**: `PascalCase` → `Usuario`, `VeiculoBase`
- **Funções/Métodos**: `snake_case` → `criar_usuario`, `listar_veiculos`
- **Constantes**: `UPPER_SNAKE_CASE` → `MAX_RETRIES`, `DATABASE_URL`
- **Variáveis**: `snake_case` → `usuario_id`, `km_atual`

### Docstrings

Use docstrings para documentar funções, classes e módulos:

```python
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """
    Cria um novo usuário no banco de dados.
    
    Args:
        db: Sessão do banco de dados SQLAlchemy
        usuario: Dados do usuário a ser criado
        
    Returns:
        Usuario: Objeto do usuário criado
        
    Raises:
        IntegrityError: Se o email já estiver cadastrado
    """
    # Implementação...
```

### Formatação de Código

Use ferramentas de formatação automática:

```bash
# Black - Formatador de código
black app/

# Flake8 - Verificação de estilo
flake8 app/

# MyPy - Verificação de tipos
mypy app/

# Pylint - Análise de código
pylint app/
```

### Configuração do Black

Crie um arquivo `pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310']
include = '\.pyi?$'
```

## 💬 Padrões de Commit

### Conventional Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]
```

### Tipos de Commit

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Mudanças na documentação
- **style**: Formatação, ponto e vírgula, etc (sem mudança de código)
- **refactor**: Refatoração de código
- **test**: Adição ou modificação de testes
- **chore**: Tarefas de manutenção (build, CI, etc)
- **perf**: Melhoria de performance

### Exemplos de Commits

```bash
# Adicionar nova funcionalidade
git commit -m "feat: adiciona endpoint de busca avançada de veículos"

# Corrigir bug
git commit -m "fix: corrige validação de email duplicado"

# Atualizar documentação
git commit -m "docs: atualiza README com instruções de deploy"

# Refatorar código
git commit -m "refactor: simplifica lógica de validação no CRUD"

# Adicionar testes
git commit -m "test: adiciona testes para endpoint de usuários"

# Commit com escopo
git commit -m "feat(auth): implementa autenticação JWT"

# Commit com breaking change
git commit -m "feat!: altera estrutura de resposta da API

BREAKING CHANGE: o campo 'usuario_id' foi renomeado para 'id_usuario'"
```

### Boas Práticas de Commit

- Use verbos no imperativo ("adiciona", não "adicionado" ou "adicionando")
- Primeira linha com máximo de 50 caracteres
- Primeira linha sem ponto final
- Use o corpo para explicar "o quê" e "por quê", não "como"
- Separe sujeito do corpo com linha em branco
- Commits pequenos e focados (um commit = uma mudança lógica)

## 🔍 Pull Requests

### Checklist Antes de Enviar

- [ ] Código segue os padrões do projeto
- [ ] Todos os testes passam (`pytest`)
- [ ] Código está formatado (`black app/`)
- [ ] Não há warnings do linter (`flake8 app/`)
- [ ] Documentação está atualizada
- [ ] Commit messages seguem o padrão
- [ ] Branch está atualizada com develop
- [ ] Não há conflitos

### Criando um Pull Request

1. **Título Claro**: Use o mesmo padrão dos commits
2. **Descrição Detalhada**:
   ```markdown
   ## Descrição
   Breve descrição das mudanças
   
   ## Motivação
   Por que esta mudança é necessária?
   
   ## Tipo de Mudança
   - [ ] Bug fix
   - [ ] Nova feature
   - [ ] Breaking change
   - [ ] Documentação
   
   ## Como Testar
   Passos para testar as mudanças
   
   ## Screenshots (se aplicável)
   
   ## Checklist
   - [ ] Testes adicionados/atualizados
   - [ ] Documentação atualizada
   - [ ] Código formatado
   ```

3. **Linkar Issues**: Use palavras-chave:
   - `Closes #123` (fecha a issue quando o PR for mergeado)
   - `Fixes #123`
   - `Resolves #123`

### Processo de Review

1. Mantenedores revisarão seu PR
2. Responda aos comentários de review
3. Faça ajustes se necessário
4. Aguarde aprovação
5. PR será mergeado por um mantenedor

### Resolvendo Conflitos

```bash
# Atualizar sua branch com develop
git checkout feature/minha-feature
git fetch origin
git rebase origin/develop

# Resolver conflitos manualmente
# Edite os arquivos com conflito

# Adicionar arquivos resolvidos
git add .

# Continuar rebase
git rebase --continue

# Force push (use com cuidado!)
git push origin feature/minha-feature --force-with-lease
```

## 🔄 Versionamento e Releases

### Versionamento Semântico

Seguimos [Semantic Versioning](https://semver.org/):

- **MAJOR**: Mudanças incompatíveis na API (1.0.0 → 2.0.0)
- **MINOR**: Novas funcionalidades compatíveis (1.0.0 → 1.1.0)
- **PATCH**: Correções de bugs compatíveis (1.0.0 → 1.0.1)

### Criando uma Release

```bash
# Atualizar develop
git checkout develop
git pull origin develop

# Criar branch de release
git checkout -b release/v1.2.0

# Atualizar CHANGELOG.md
# Atualizar versão em arquivos necessários

# Commit mudanças
git commit -m "chore: prepara release v1.2.0"

# Merge em main
git checkout main
git merge release/v1.2.0

# Criar tag
git tag -a v1.2.0 -m "Release v1.2.0"

# Push main e tags
git push origin main
git push origin --tags

# Merge de volta em develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# Deletar branch de release
git branch -d release/v1.2.0
```

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app tests/

# Teste específico
pytest tests/test_usuarios.py

# Com output verboso
pytest -v

# Parar no primeiro erro
pytest -x
```

### Escrevendo Testes

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_usuario():
    """Testa criação de novo usuário."""
    response = client.post(
        "/usuarios/",
        json={
            "nome": "Teste",
            "email": "teste@exemplo.com",
            "senha": "senha123"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "teste@exemplo.com"
```

## 📚 Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Python PEP 8](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 💡 Dicas Finais

- Comunique-se! Use as issues e PRs para discussões
- Peça ajuda quando necessário
- Seja paciente com reviews - qualidade leva tempo
- Aprenda com o feedback
- Mantenha PRs pequenos e focados
- Teste localmente antes de enviar

## 🙋 Dúvidas?

Se você tiver dúvidas sobre como contribuir:

1. Leia a documentação existente
2. Procure em issues fechadas
3. Abra uma nova issue com sua dúvida
4. Entre em contato com os mantenedores

---

**Obrigado por contribuir! 🎉**
