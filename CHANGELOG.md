# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.3.0] - 2024-11-19

### ✨ Adicionado

#### Dashboard
- Dashboard completamente redesenhado com estatísticas em tempo real
- Cards mostrando total de veículos, manutenções e custos
- Cards de acesso rápido às principais funcionalidades
- Cards informativos com dicas de uso e recursos do sistema
- Botão "Atualizar" para recarregar estatísticas

#### Interface
- Menu lateral unificado presente em todas as páginas
- Ícones intuitivos no menu (🏠 Início, 🚗 Veículos, 🔧 Manutenção, etc.)
- Modal de edição inline para veículos
- Modal de edição inline para manutenções
- Modal de confirmação para exclusão de veículos
- Modal de confirmação para exclusão de manutenções
- Página "Meus Veículos" com listagem completa

#### Funcionalidades
- Filtro por placa na lista de veículos
- Filtro por placa no relatório de manutenções
- Botão "Limpar Filtro" em ambas as páginas
- Placa desabilitada no formulário de edição (não editável)
- Atualização automática das listas após edição/exclusão

#### Scripts
- `install.bat` - Script de instalação automatizada (Windows)
- `start.bat` - Script de inicialização do servidor (Windows)

### 🎨 Melhorado

#### Design
- Estrutura HTML usando herança de templates (`base.html`)
- Fonte Barlow do Google Fonts em todo o sistema
- Cores consistentes em todas as páginas
- Espaçamentos e margens padronizados
- Responsividade mobile aprimorada
- Animações suaves em modais e transições

#### Código
- JavaScript organizado com logs detalhados
- Event listeners otimizados (sem duplicação)
- Funções reutilizáveis para modais
- Validações de formulário aprimoradas
- Tratamento de erros mais robusto

#### UX/UI
- Feedback visual imediato em todas as ações
- Mensagens de sucesso/erro mais claras
- Loading states durante requisições
- Confirmações antes de ações destrutivas

### 🔧 Corrigido

- **Bug crítico:** Modais aparecendo automaticamente ao carregar páginas
- **Bug:** Event listeners duplicados causando múltiplas ações
- **Bug:** Estrutura HTML incorreta no `manutencao_report.html`
- **Bug:** Filtros não aplicando corretamente
- **Bug:** Placa sendo editável no formulário de edição
- **Bug:** Lista não atualizando após exclusão
- **Bug:** Modal não fechando ao pressionar ESC
- **Bug:** Formatação de valores monetários inconsistente

### 📝 Documentação

- README.md completo com badges e estrutura profissional
- INSTALL.md com guia detalhado de instalação
- CHANGELOG.md com histórico de versões
- .env.example com template de configuração
- Comentários detalhados no código JavaScript
- Logs de debug para facilitar troubleshooting

### 🗄️ Banco de Dados

- Validações aprimoradas nos modelos SQLAlchemy
- Índices otimizados para consultas
- Relacionamentos entre tabelas refinados

---

## [1.2.0] - 2024-11-15

### ✨ Adicionado

- Sistema de relatórios de manutenções com filtros
- Filtro por veículo no relatório
- Exportação básica de dados
- Paginação na lista de manutenções
- Busca por período de manutenções

### 🎨 Melhorado

- Performance das consultas ao banco
- Interface de listagem de manutenções
- Validações de formulários
- Mensagens de erro mais descritivas

### 🔧 Corrigido

- Bug na autenticação ao fazer logout
- Problema de validação de datas
- Erro ao cadastrar manutenção com valores decimais
- Conflito de CSS entre páginas

---

## [1.1.0] - 2024-11-10

### ✨ Adicionado

- CRUD completo de manutenções
- Formulário de registro de manutenções
- Associação de manutenções com veículos
- Validação de quilometragem progressiva
- Campo de observações nas manutenções
- Página de visualização de manutenções por veículo

### 🎨 Melhorado

- Navegação entre páginas
- Layout dos formulários
- Validações de campos obrigatórios

### 🔧 Corrigido

- Erro ao deletar veículo com manutenções associadas
- Problema de encoding em caracteres especiais
- Bug no formulário de edição de veículos

---

## [1.0.0] - 2024-11-05

### ✨ Inicial

#### Autenticação
- Sistema de autenticação com JWT
- Registro de novos usuários
- Login com email e senha
- Logout com limpeza de token
- Proteção de rotas autenticadas

#### Veículos
- CRUD completo de veículos
- Validação de placa única
- Campos: placa, marca, modelo, ano, quilometragem
- Listagem de veículos do usuário
- Formulário de cadastro
- Edição de veículos
- Exclusão de veículos

#### Interface
- Template base com Jinja2
- Página de login responsiva
- Página de registro
- Dashboard básico
- Menu de navegação
- Estilos CSS customizados

#### Backend
- FastAPI como framework web
- SQLAlchemy como ORM
- PostgreSQL como banco de dados
- Pydantic para validação de dados
- Bcrypt para hash de senhas
- Estrutura modular com rotas separadas

#### Banco de Dados
- Modelo de Usuários
- Modelo de Veículos
- Modelo de Planos
- Relacionamentos entre tabelas
- Migrações automáticas

---

## [Unreleased] - Planejado para Próximas Versões

### 🚀 Versão 1.4.0

#### Features Planejadas
- [ ] Exportação de relatórios em PDF
- [ ] Gráficos de custos mensais com Chart.js
- [ ] Notificações de manutenções próximas
- [ ] Upload de fotos dos veículos
- [ ] Histórico de alterações (audit log)
- [ ] Backup automático do banco de dados
- [ ] API pública com documentação Swagger expandida
- [ ] Filtros avançados por data e tipo de manutenção

#### Melhorias Planejadas
- [ ] Performance otimizada nas consultas
- [ ] Cache de estatísticas do dashboard
- [ ] Compressão de imagens
- [ ] Lazy loading de listas grandes

#### Testes
- [ ] Testes unitários com pytest
- [ ] Testes de integração
- [ ] Testes end-to-end
- [ ] Cobertura de código >80%

### 🔮 Versão 2.0.0

#### Features Futuras
- [ ] App mobile com React Native
- [ ] Notificações por email
- [ ] Lembretes automáticos de manutenção
- [ ] Integração com agenda (Google Calendar)
- [ ] Múltiplos usuários por veículo (compartilhamento)
- [ ] Modo escuro (dark mode)
- [ ] Suporte a múltiplos idiomas (i18n)
- [ ] Sistema de gamificação (badges, conquistas)
- [ ] Integração com oficinas parceiras
- [ ] Agendamento de manutenções

#### Infraestrutura
- [ ] Deploy em Docker
- [ ] CI/CD com GitHub Actions
- [ ] Monitoramento com Prometheus/Grafana
- [ ] Logs centralizados
- [ ] Ambiente de staging

---

## 📊 Estatísticas de Versões

| Versão | Data | Commits | Arquivos Alterados | Linhas Adicionadas | Linhas Removidas |
|--------|------|---------|--------------------|--------------------|------------------|
| 1.3.0 | 2024-11-19 | 15 | 25 | +2.500 | -800 |
| 1.2.0 | 2024-11-15 | 10 | 18 | +1.200 | -300 |
| 1.1.0 | 2024-11-10 | 8 | 12 | +900 | -150 |
| 1.0.0 | 2024-11-05 | 20 | 30 | +3.000 | -0 |

---

## 🏷️ Convenções de Versionamento

Este projeto segue o [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Mudanças incompatíveis com versões anteriores
- **MINOR** (x.X.0): Novas funcionalidades mantendo compatibilidade
- **PATCH** (x.x.X): Correções de bugs mantendo compatibilidade

### Exemplos:
- `1.0.0` → `1.1.0`: Nova funcionalidade (manutenções)
- `1.1.0` → `1.1.1`: Correção de bug
- `1.3.0` → `2.0.0`: Mudança incompatível (API breaking change)

---

## 🔗 Links

- [Repositório GitHub](https://github.com/GuilhemeMiranda/Python_Projetos)
- [Releases](https://github.com/GuilhemeMiranda/Python_Projetos/releases)
- [Issues](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- [Pull Requests](https://github.com/GuilhemeMiranda/Python_Projetos/pulls)

---

**Mantenha este arquivo atualizado a cada nova versão!**

[1.3.0]: https://github.com/GuilhemeMiranda/Python_Projetos/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/GuilhemeMiranda/Python_Projetos/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/GuilhemeMiranda/Python_Projetos/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/GuilhemeMiranda/Python_Projetos/releases/tag/v1.0.0