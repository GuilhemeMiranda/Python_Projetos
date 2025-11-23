# Guia de Comandos Git

Este documento fornece uma referência rápida dos comandos Git mais utilizados no projeto.

## 📚 Índice

1. [Configuração Inicial](#configuração-inicial)
2. [Clonando o Repositório](#clonando-o-repositório)
3. [Trabalhando com Branches](#trabalhando-com-branches)
4. [Fazendo Commits](#fazendo-commits)
5. [Sincronizando com Remoto](#sincronizando-com-remoto)
6. [Resolvendo Conflitos](#resolvendo-conflitos)
7. [Histórico e Inspeção](#histórico-e-inspeção)
8. [Desfazendo Mudanças](#desfazendo-mudanças)
9. [Tags e Releases](#tags-e-releases)
10. [Comandos Avançados](#comandos-avançados)

## 🔧 Configuração Inicial

### Configurar seu nome e email
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### Verificar configuração
```bash
git config --list
```

### Configurar editor padrão
```bash
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim
```

### Habilitar cores no terminal
```bash
git config --global color.ui auto
```

## 📥 Clonando o Repositório

### Clone básico
```bash
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git
cd Python_Projetos
```

### Clone de branch específica
```bash
git clone -b develop https://github.com/GuilhemeMiranda/Python_Projetos.git
```

### Clone raso (sem histórico completo)
```bash
git clone --depth 1 https://github.com/GuilhemeMiranda/Python_Projetos.git
```

## 🌿 Trabalhando com Branches

### Listar branches
```bash
git branch              # Locais
git branch -r           # Remotas
git branch -a           # Todas
```

### Criar nova branch
```bash
git checkout -b feature/minha-funcionalidade
# ou
git branch feature/minha-funcionalidade
git checkout feature/minha-funcionalidade
```

### Mudar de branch
```bash
git checkout develop
# ou (Git 2.23+)
git switch develop
```

### Criar branch a partir de commit específico
```bash
git checkout -b hotfix/bug-critico abc1234
```

### Deletar branch
```bash
git branch -d feature/antiga          # Deleta se já foi mergeada
git branch -D feature/antiga          # Force delete
git push origin --delete feature/antiga  # Deletar no remoto
```

### Renomear branch
```bash
git branch -m nome-antigo nome-novo
# Se estiver na branch:
git branch -m novo-nome
```

## 💾 Fazendo Commits

### Ver status das mudanças
```bash
git status
git status -s  # Formato compacto
```

### Ver diferenças
```bash
git diff                    # Mudanças não staged
git diff --staged           # Mudanças staged
git diff HEAD               # Todas as mudanças
git diff branch1 branch2    # Entre branches
```

### Adicionar arquivos
```bash
git add arquivo.py                 # Arquivo específico
git add app/                       # Diretório
git add .                          # Todos os arquivos
git add -p                         # Interativo (patch mode)
git add *.py                       # Por padrão
```

### Fazer commit
```bash
git commit -m "feat: adiciona nova funcionalidade"
git commit -am "fix: corrige bug"  # Add + commit (apenas rastreados)
```

### Commit com corpo detalhado
```bash
git commit -m "feat: adiciona autenticação JWT" -m "
- Implementa geração de tokens
- Adiciona middleware de autenticação
- Cria endpoints de login/logout
"
```

### Alterar último commit
```bash
git commit --amend -m "Nova mensagem"
git commit --amend --no-edit  # Adicionar arquivos sem mudar mensagem
```

## 🔄 Sincronizando com Remoto

### Adicionar remote
```bash
git remote add origin https://github.com/GuilhemeMiranda/Python_Projetos.git
```

### Listar remotes
```bash
git remote -v
```

### Buscar atualizações (não aplica)
```bash
git fetch origin
git fetch --all
```

### Baixar e mesclar mudanças (pull)
```bash
git pull origin develop
git pull --rebase origin develop  # Usa rebase em vez de merge
```

### Enviar mudanças (push)
```bash
git push origin feature/minha-funcionalidade
git push -u origin feature/minha-funcionalidade  # Define upstream
git push --force-with-lease  # Force push seguro
```

### Atualizar branch local com remota
```bash
git checkout develop
git pull origin develop
```

## ⚔️ Resolvendo Conflitos

### Workflow para resolver conflitos
```bash
# 1. Tentar pull/merge
git pull origin develop

# 2. Se houver conflito, Git mostrará os arquivos
git status

# 3. Editar arquivos com conflito manualmente
# Procure por marcadores: <<<<<<<, =======, >>>>>>>

# 4. Adicionar arquivos resolvidos
git add arquivo_resolvido.py

# 5. Continuar merge
git commit

# 6. Push das mudanças
git push origin feature/minha-branch
```

### Ferramentas de merge
```bash
# Usar ferramenta visual de merge
git mergetool

# Abortar merge
git merge --abort

# Aceitar versão deles
git checkout --theirs arquivo.py
git add arquivo.py

# Aceitar sua versão
git checkout --ours arquivo.py
git add arquivo.py
```

## 🔍 Histórico e Inspeção

### Ver log de commits
```bash
git log                           # Completo
git log --oneline                 # Compacto
git log --graph --all --oneline   # Gráfico
git log -n 5                      # Últimos 5
git log --author="João"           # Por autor
git log --since="2 weeks ago"     # Por data
git log --grep="fix"              # Por mensagem
```

### Ver log de arquivo específico
```bash
git log arquivo.py
git log -p arquivo.py  # Com diff
```

### Ver commit específico
```bash
git show abc1234
git show HEAD
git show HEAD~2  # 2 commits atrás
```

### Ver quem modificou cada linha
```bash
git blame arquivo.py
git blame -L 10,20 arquivo.py  # Linhas específicas
```

### Ver mudanças de branch
```bash
git log develop..feature/nova  # Commits em feature que não estão em develop
```

## ⏪ Desfazendo Mudanças

### Descartar mudanças não staged
```bash
git restore arquivo.py           # Git 2.23+
git checkout -- arquivo.py       # Versão antiga
git restore .                    # Todos os arquivos
```

### Unstage arquivos
```bash
git restore --staged arquivo.py  # Git 2.23+
git reset HEAD arquivo.py        # Versão antiga
```

### Desfazer último commit (mantém mudanças)
```bash
git reset --soft HEAD~1
```

### Desfazer último commit (descarta mudanças)
```bash
git reset --hard HEAD~1  # ⚠️ CUIDADO: Perde alterações!
```

### Reverter commit (cria novo commit)
```bash
git revert abc1234
git revert HEAD
```

### Limpar arquivos não rastreados
```bash
git clean -n   # Dry run (mostra o que seria removido)
git clean -f   # Remove arquivos
git clean -fd  # Remove arquivos e diretórios
```

### Resetar para estado remoto
```bash
git fetch origin
git reset --hard origin/develop  # ⚠️ CUIDADO: Perde alterações locais!
```

## 🏷️ Tags e Releases

### Listar tags
```bash
git tag
git tag -l "v1.*"  # Filtrar
```

### Criar tag
```bash
# Tag anotada (recomendada)
git tag -a v1.0.0 -m "Release 1.0.0"

# Tag leve
git tag v1.0.0

# Tag em commit específico
git tag -a v1.0.0 abc1234 -m "Release 1.0.0"
```

### Enviar tags
```bash
git push origin v1.0.0     # Tag específica
git push origin --tags     # Todas as tags
git push --follow-tags     # Tags de commits pushados
```

### Deletar tag
```bash
git tag -d v1.0.0                # Local
git push origin --delete v1.0.0  # Remota
```

### Ver informações de tag
```bash
git show v1.0.0
```

## 🚀 Comandos Avançados

### Stash (guardar mudanças temporariamente)
```bash
git stash                      # Guardar mudanças
git stash save "mensagem"      # Com mensagem
git stash list                 # Listar stashes
git stash apply                # Aplicar último stash
git stash apply stash@{2}      # Aplicar stash específico
git stash pop                  # Aplicar e remover último
git stash drop stash@{1}       # Remover stash
git stash clear                # Remover todos
```

### Cherry-pick (aplicar commit específico)
```bash
git cherry-pick abc1234
git cherry-pick abc1234 def5678  # Múltiplos commits
```

### Rebase
```bash
# Rebase interativo (últimos 3 commits)
git rebase -i HEAD~3

# Rebase em outra branch
git rebase develop

# Continuar após resolver conflitos
git rebase --continue

# Abortar rebase
git rebase --abort
```

### Bisect (encontrar commit com bug)
```bash
git bisect start
git bisect bad                 # Commit atual tem bug
git bisect good v1.0.0        # Tag sem bug
# Git vai sugerindo commits para testar
git bisect good/bad           # Marcar cada teste
git bisect reset              # Finalizar
```

### Reflog (histórico de mudanças HEAD)
```bash
git reflog
git reflog show develop
```

### Submodules
```bash
git submodule add https://github.com/user/repo.git path/to/submodule
git submodule update --init --recursive
git submodule update --remote
```

### Worktree (múltiplas working trees)
```bash
git worktree add ../projeto-hotfix hotfix/urgent-fix
git worktree list
git worktree remove ../projeto-hotfix
```

## 📝 Dicas e Boas Práticas

### Aliases úteis
Adicione ao `.gitconfig`:
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --graph --oneline --all"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
```

### .gitignore global
```bash
git config --global core.excludesfile ~/.gitignore_global
```

### Verificar antes de push
```bash
git log origin/develop..HEAD   # Ver commits que serão enviados
git diff origin/develop HEAD   # Ver mudanças que serão enviadas
```

### Buscar texto no histórico
```bash
git log -S "texto_procurado"
git log -G "regex_pattern"
```

## 🆘 Ajuda

### Obter ajuda
```bash
git help <comando>
git <comando> --help
man git-<comando>
```

### Exemplos
```bash
git help commit
git log --help
```

## 📚 Recursos Adicionais

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)

---

**Criado por:** Guilherme Miranda  
**Última atualização:** Novembro 2024
