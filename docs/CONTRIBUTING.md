# 🤝 Guia de Contribuição - Sistema de Manutenção Veicular

Obrigado por considerar contribuir com o Sistema de Manutenção Veicular! Este documento fornece diretrizes para contribuir com o projeto.

---

## 📋 Índice

1. [Código de Conduta](#-código-de-conduta)
2. [Como Posso Contribuir?](#-como-posso-contribuir)
3. [Primeiros Passos](#-primeiros-passos)
4. [Processo de Desenvolvimento](#-processo-de-desenvolvimento)
5. [Padrões de Código](#-padrões-de-código)
6. [Padrões de Commits](#-padrões-de-commits)
7. [Pull Requests](#-pull-requests)
8. [Reportando Bugs](#-reportando-bugs)
9. [Sugerindo Features](#-sugerindo-features)
10. [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 📜 Código de Conduta

Este projeto adota um Código de Conduta que esperamos que todos os participantes sigam.

### Nossos Valores

- ✅ Seja respeitoso e inclusivo
- ✅ Aceite críticas construtivas
- ✅ Foque no que é melhor para a comunidade
- ✅ Mostre empatia com outros membros

### Comportamentos Inaceitáveis

- ❌ Linguagem ou imagens sexualizadas
- ❌ Comentários insultuosos ou depreciativos
- ❌ Assédio público ou privado
- ❌ Publicar informações privadas de outros
- ❌ Conduta não profissional

---

## 💡 Como Posso Contribuir?

Existem várias formas de contribuir:

### 1. 🐛 Reportar Bugs

Encontrou um bug? Ajude-nos reportando!

- Verifique se o bug já não foi reportado nas [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- Se não encontrar, crie uma nova issue
- Use o template de bug report
- Inclua o máximo de detalhes possível

### 2. 💡 Sugerir Features

Tem uma ideia para melhorar o sistema?

- Verifique se já não foi sugerida
- Crie uma issue com o label "enhancement"
- Descreva claramente a feature e seus benefícios
- Adicione mockups se possível

### 3. 📝 Melhorar Documentação

Documentação nunca é demais!

- Corrija erros de português
- Adicione exemplos
- Melhore explicações
- Traduza para outros idiomas

### 4. 💻 Contribuir com Código

Desenvolvimento é sempre bem-vindo!

- Correções de bugs
- Novas features
- Melhorias de performance
- Refatoração de código
- Testes automatizados

### 5. 🎨 Design e UX

Ajude a melhorar a interface!

- Melhorias de design
- Ícones e imagens
- Responsividade
- Acessibilidade

---

## 🚀 Primeiros Passos

### 1. Fork o Repositório

Clique no botão "Fork" no canto superior direito da página do repositório.

### 2. Clone seu Fork

```bash
git clone https://github.com/SEU_USUARIO/Python_Projetos.git
cd Python_Projetos/Manutencao_Veicular
```

### 3. Configure o Remote Upstream

```bash
git remote add upstream https://github.com/GuilhemeMiranda/Python_Projetos.git
```

### 4. Crie um Branch

```bash
# Atualize seu main
git checkout main
git pull upstream main

# Crie um branch para sua feature
git checkout -b feature/minha-feature
```

### 5. Configure o Ambiente

Siga o [Guia de Instalação](../INSTALL.md) para configurar o ambiente de desenvolvimento.

---

## 🔧 Processo de Desenvolvimento

### 1. Escolha uma Issue

- Verifique as [issues abertas](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- Issues marcadas com `good first issue` são ideais para iniciantes
- Comente na issue dizendo que vai trabalhar nela

### 2. Desenvolva

```bash
# Crie seu branch
git checkout -b feature/nome-da-feature

# Faça suas alterações
# ...

# Teste suas alterações
pytest

# Commit suas mudanças
git add .
git commit -m "feat: adiciona nova funcionalidade"
```

### 3. Mantenha seu Branch Atualizado

```bash
# Busque as últimas mudanças
git fetch upstream

# Faça rebase com o main
git rebase upstream/main

# Resolva conflitos se necessário
```

### 4. Push para seu Fork

```bash
git push origin feature/nome-da-feature
```

### 5. Abra um Pull Request

- Vá até seu fork no GitHub
- Clique em "Compare & pull request"
- Preencha o template de PR
- Aguarde review

---

## 📏 Padrões de Código

### Python (Backend)

Seguimos a [PEP 8](https://pep8.org/):

```python
# ✅ BOM
def calcular_custo_total(manutencoes):
    """Calcula o custo total das manutenções.
    
    Args:
        manutencoes (List[Manutencao]): Lista de manutenções
        
    Returns:
        float: Custo total
    """
    return sum(m.custo for m in manutencoes)


# ❌ RUIM
def calc(m):
    return sum(x.custo for x in m)
```

#### Convenções

- **Indentação:** 4 espaços (não tabs)
- **Linhas:** Máximo 88 caracteres (Black formatter)
- **Imports:** Organizados (stdlib, terceiros, locais)
- **Docstrings:** Use Google Style
- **Type Hints:** Use sempre que possível

```python
from typing import List, Optional
from datetime import date

def criar_manutencao(
    veiculo_id: int,
    data: date,
    km: int,
    tipo: str,
    custo: float,
    observacoes: Optional[str] = None
) -> Manutencao:
    """Cria uma nova manutenção."""
    pass
```

### JavaScript (Frontend)

Seguimos o [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript):

```javascript
// ✅ BOM
async function buscarVeiculos() {
  try {
    const response = await fetch('/veiculos/');
    const veiculos = await response.json();
    return veiculos;
  } catch (error) {
    console.error('Erro ao buscar veículos:', error);
    throw error;
  }
}

// ❌ RUIM
function getVeic() {
  fetch('/veiculos/').then(r => r.json()).then(v => console.log(v));
}
```

#### Convenções

- **Indentação:** 2 espaços
- **Strings:** Use aspas simples `'`
- **Variáveis:** Use `const` por padrão, `let` quando necessário
- **Funções:** Prefira arrow functions
- **Async/Await:** Use ao invés de `.then()`

### HTML/CSS

```html
<!-- ✅ BOM -->
<div class="card card-veiculos">
  <h3 class="card-title">Meus Veículos</h3>
  <p class="card-description">Gerencie seus veículos</p>
</div>
```

```css
/* ✅ BOM */
.card {
  padding: 1.5rem;
  border-radius: 8px;
  background-color: var(--cor-primaria);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
```

#### Convenções

- **Classes:** Use kebab-case
- **IDs:** Use kebab-case
- **Indentação:** 2 espaços
- **Semântica:** Use tags HTML5 semânticas

---

## 📝 Padrões de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

### Formato

```
<tipo>(<escopo>): <descrição curta>

<descrição detalhada (opcional)>

<footer (opcional)>
```

### Tipos

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat: adiciona filtro por data` |
| `fix` | Correção de bug | `fix: corrige erro ao deletar veículo` |
| `docs` | Documentação | `docs: atualiza README` |
| `style` | Formatação (sem mudança de código) | `style: formata código com black` |
| `refactor` | Refatoração | `refactor: simplifica função de cálculo` |
| `test` | Adiciona testes | `test: adiciona testes para API` |
| `chore` | Tarefas de manutenção | `chore: atualiza dependências` |
| `perf` | Melhoria de performance | `perf: otimiza query SQL` |

### Exemplos

```bash
# Feature simples
git commit -m "feat: adiciona exportação em PDF"

# Feature com escopo
git commit -m "feat(veiculos): adiciona upload de fotos"

# Bug fix com descrição
git commit -m "fix: corrige erro ao editar manutenção

O modal não fechava após salvar. Adicionado listener
para fechar após resposta bem-sucedida da API."

# Breaking change
git commit -m "feat!: muda estrutura da API

BREAKING CHANGE: endpoint /veiculos agora retorna array
de objetos ao invés de objeto com array."
```

### Regras

- ✅ Use o imperativo ("adiciona" não "adicionado")
- ✅ Primeira linha com máximo 72 caracteres
- ✅ Corpo do commit com máximo 100 caracteres por linha
- ✅ Descreva O QUE e POR QUE, não COMO
- ✅ Referencie issues quando aplicável: `Closes #123`

---

## 🔀 Pull Requests

### Antes de Abrir um PR

- [ ] Código segue os padrões do projeto
- [ ] Todos os testes passam
- [ ] Documentação foi atualizada
- [ ] Commits seguem o padrão Conventional Commits
- [ ] Branch está atualizado com `main`
- [ ] Não há conflitos

### Template de PR

```markdown
## Descrição

Descreva o que este PR faz.

## Tipo de Mudança

- [ ] 🐛 Bug fix
- [ ] ✨ Nova feature
- [ ] 💥 Breaking change
- [ ] 📝 Documentação
- [ ] 🎨 Estilo/UI

## Como Testar

1. Faça checkout deste branch
2. Execute `uvicorn app.main:app --reload`
3. Acesse http://localhost:8000
4. ...

## Checklist

- [ ] Meu código segue os padrões do projeto
- [ ] Realizei self-review do meu código
- [ ] Comentei partes complexas
- [ ] Atualizei a documentação
- [ ] Minhas mudanças não geram novos warnings
- [ ] Adicionei testes que provam que meu fix funciona
- [ ] Todos os testes passam localmente
- [ ] Atualizei o CHANGELOG.md

## Screenshots (se aplicável)

Adicione screenshots mostrando as mudanças visuais.

## Issues Relacionadas

Closes #123
Relates to #456
```

### Processo de Review

1. **Autor abre PR** → Preenche template
2. **CI/CD executa** → Testes automáticos
3. **Reviewer analisa** → Sugere mudanças
4. **Autor ajusta** → Faz correções
5. **Reviewer aprova** → Dá OK
6. **Mantenedor merge** → PR é integrado

### O que os Reviewers Avaliam

- ✅ Código funciona e resolve o problema
- ✅ Testes adequados foram adicionados
- ✅ Documentação foi atualizada
- ✅ Código está limpo e legível
- ✅ Não introduz bugs ou regressões
- ✅ Performance não foi degradada

---

## 🐛 Reportando Bugs

### Antes de Reportar

1. Verifique se não é uma issue conhecida
2. Tente reproduzir em ambiente limpo
3. Colete informações relevantes

### Template de Bug Report

```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Como Reproduzir**
Passos para reproduzir:
1. Vá para '...'
2. Clique em '...'
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Comportamento Atual**
O que está acontecendo.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [ex: Windows 10]
- Navegador: [ex: Chrome 119]
- Python: [ex: 3.9.0]
- PostgreSQL: [ex: 13.3]

**Logs de Erro**
```
Cole aqui os logs/erros
```

**Contexto Adicional**
Qualquer outra informação relevante.
```

---

## 💡 Sugerindo Features

### Template de Feature Request

```markdown
**A feature está relacionada a um problema?**
Descrição clara do problema. Ex: "Sempre fico frustrado quando..."

**Descreva a solução desejada**
Descrição clara do que você quer que aconteça.

**Descreva alternativas consideradas**
Outras soluções ou features que você considerou.

**Benefícios**
Por que esta feature seria útil?
- Para usuários finais
- Para desenvolvedores
- Para o projeto

**Mockups/Exemplos**
Se aplicável, adicione mockups ou exemplos.

**Contexto Adicional**
Qualquer outra informação ou screenshots.
```

---

## 📁 Estrutura do Projeto

### Backend (Python/FastAPI)

```
app/
├── __init__.py
├── main.py              # Ponto de entrada
├── database.py          # Configuração do banco
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── crud.py              # Operações CRUD
├── security.py          # Autenticação JWT
└── routes/              # Rotas da API
    ├── auth.py
    ├── veiculos.py
    ├── manutencoes.py
    └── ...
```

### Frontend (HTML/CSS/JS)

```
app/
├── static/              # Arquivos estáticos
│   ├── styles.css      # Estilos globais
│   ├── app.js          # JavaScript global
│   └── ...
└── templates/           # Templates Jinja2
    ├── base.html       # Template base
    ├── index.html      # Dashboard
    └── ...
```

### Testes

```
tests/
├── __init__.py
├── test_auth.py
├── test_veiculos.py
├── test_manutencoes.py
└── conftest.py
```

---

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app tests/

# Testes específicos
pytest tests/test_auth.py

# Modo verbose
pytest -v

# Para na primeira falha
pytest -x
```

### Escrevendo Testes

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_veiculo():
    """Testa criação de veículo."""
    # Arrange
    token = login_usuario()
    veiculo_data = {
        "placa": "ABC1234",
        "marca": "Ford",
        "modelo": "Fiesta",
        "ano": 2020,
        "km_atual": 45000
    }
    
    # Act
    response = client.post(
        "/veiculos/",
        json=veiculo_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert
    assert response.status_code == 201
    assert response.json()["placa"] == "ABC1234"
```

---

## 🛠️ Ferramentas Úteis

### Formatadores

```bash
# Black (Python formatter)
pip install black
black app/

# isort (organiza imports)
pip install isort
isort app/

# Prettier (JS/CSS/HTML formatter)
npm install -g prettier
prettier --write app/static/**/*.js
```

### Linters

```bash
# flake8 (Python linter)
pip install flake8
flake8 app/

# pylint (Python linter)
pip install pylint
pylint app/

# ESLint (JavaScript linter)
npm install -g eslint
eslint app/static/**/*.js
```

### Type Checkers

```bash
# mypy (Python type checker)
pip install mypy
mypy app/
```

---

## 📞 Precisa de Ajuda?

### Recursos

- 📖 [README.md](../README.md)
- 📥 [INSTALL.md](../INSTALL.md)
- 🔌 [API.md](API.md)
- 🐛 [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- 💬 [Discussions](https://github.com/GuilhemeMiranda/Python_Projetos/discussions)

### Contato

- GitHub: [@GuilhemeMiranda](https://github.com/GuilhemeMiranda)
- Email: contato@exemplo.com

---

## 🎉 Agradecimentos

Obrigado por contribuir! Cada contribuição, por menor que seja, faz diferença. 💙

### Top Contribuidores

<!-- Será atualizado automaticamente -->

---

## 📜 Licença

Ao contribuir com este projeto, você concorda que suas contribuições serão licenciadas sob a [Licença MIT](../LICENSE).

---

**Desenvolvido com ❤️ pela comunidade**

**Mantido por [Guilherme Miranda](https://github.com/GuilhemeMiranda)**