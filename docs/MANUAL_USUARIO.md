# 📖 Manual do Usuário - Sistema de Manutenção Veicular

Guia completo para usar todas as funcionalidades do sistema.

---

## 📋 Índice

1. [Primeiros Passos](#-primeiros-passos)
2. [Criando sua Conta](#-criando-sua-conta)
3. [Fazendo Login](#-fazendo-login)
4. [Dashboard](#-dashboard)
5. [Gerenciando Veículos](#-gerenciando-veículos)
6. [Registrando Manutenções](#-registrando-manutenções)
7. [Relatórios](#-relatórios)
8. [Dicas e Truques](#-dicas-e-truques)
9. [Perguntas Frequentes](#-perguntas-frequentes)
10. [Solução de Problemas](#-solução-de-problemas)

---

## 🚀 Primeiros Passos

### Acessando o Sistema

1. Abra seu navegador (Chrome, Firefox, Edge ou Safari)
2. Digite na barra de endereços: `http://localhost:8000/ui/login`
3. Pressione Enter

### Requisitos

- ✅ Navegador atualizado
- ✅ Conexão com internet (apenas para fontes)
- ✅ JavaScript habilitado

---

## 👤 Criando sua Conta

### Passo a Passo

1. **Na tela de login**, clique em **"Criar nova conta"**

2. **Preencha o formulário**:
   - **Nome:** Seu nome completo
   - **Email:** Um endereço de email válido
   - **Senha:** Mínimo 6 caracteres
   - **Confirmar Senha:** Digite a senha novamente

3. **Clique em "Cadastrar"**

4. **Aguarde a confirmação**:
   - ✅ "Usuário cadastrado com sucesso!"
   - Você será redirecionado para a tela de login

### Dicas de Senha

- ✅ Use letras maiúsculas e minúsculas
- ✅ Inclua números
- ✅ Use caracteres especiais (@, #, $, etc.)
- ✅ Mínimo 8 caracteres
- ❌ Não use senhas óbvias (123456, senha123)

---

## 🔐 Fazendo Login

### Passo a Passo

1. **Digite seu email** cadastrado
2. **Digite sua senha**
3. **Clique em "Entrar"**

### O que acontece após o login?

- ✅ Você é redirecionado para o **Dashboard**
- ✅ Um token de autenticação é criado
- ✅ O token expira em 30 minutos de inatividade

### Esqueci minha senha

⚠️ **Funcionalidade em desenvolvimento**

Por enquanto, entre em contato com o administrador do sistema.

---

## 📊 Dashboard

O Dashboard é a página principal do sistema. Aqui você tem uma visão geral de tudo.

### Estatísticas

O topo da página mostra 3 cards com estatísticas:

1. **Total de Veículos** 🚗
   - Quantidade de veículos cadastrados

2. **Manutenções Registradas** 🔧
   - Total de manutenções no sistema

3. **Custo Total** 💰
   - Soma de todos os custos de manutenções
   - Formatado em Reais (R$)

### Cards de Acesso Rápido

Abaixo das estatísticas, você encontra cards para acessar rapidamente:

- **Cadastrar Veículo** 🚗
  - Adicione um novo veículo

- **Registrar Manutenção** 🔧
  - Registre uma nova manutenção

- **Meus Veículos** 📋
  - Veja lista completa de veículos

- **Relatório de Manutenções** 📊
  - Visualize e filtre manutenções

### Botão Atualizar

- Clique em **"🔄 Atualizar"** para recarregar as estatísticas

---

## 🚗 Gerenciando Veículos

### Cadastrar Novo Veículo

#### Passo a Passo

1. No **Dashboard**, clique em **"Cadastrar Veículo"**
   - Ou no menu lateral: **Veículos → Novo Veículo**

2. **Preencha o formulário**:
   - **Placa:** ABC1234 ou ABC-1234
   - **Marca:** Ex: Ford, Fiat, Volkswagen
   - **Modelo:** Ex: Fiesta, Uno, Gol
   - **Ano:** Ano de fabricação (ex: 2020)
   - **KM Atual:** Quilometragem atual (ex: 45000)

3. **Clique em "Salvar"**

4. **Aguarde a confirmação**:
   - ✅ "Veículo cadastrado com sucesso!"
   - Você será redirecionado para a lista de veículos

#### Validações

- ❌ **Placa única:** Não pode cadastrar a mesma placa duas vezes
- ❌ **Ano:** Deve ser entre 1900 e o ano atual
- ❌ **KM:** Deve ser um número positivo

---

### Listar Veículos

#### Passo a Passo

1. No menu lateral, clique em **"Meus Veículos"**

2. **Você verá uma tabela** com todos os seus veículos:
   - Placa
   - Marca/Modelo
   - Ano
   - KM Atual
   - Ações (Editar/Excluir)

#### Filtrar por Placa

1. Digite a placa no campo **"Filtrar por placa"**
2. Clique em **"Filtrar"**
3. Para limpar o filtro, clique em **"Limpar Filtro"**

---

### Editar Veículo

#### Passo a Passo

1. Na lista de veículos, clique no botão **"✏️ Editar"**

2. **Um modal se abrirá** com os dados do veículo

3. **Edite os campos desejados**:
   - ⚠️ **Placa não pode ser alterada**
   - Marca
   - Modelo
   - Ano
   - KM Atual

4. **Clique em "Salvar"**

5. **O modal fecha** e a lista é atualizada automaticamente

#### Cancelar Edição

- Clique em **"Cancelar"** ou
- Pressione **ESC** ou
- Clique fora do modal

---

### Excluir Veículo

#### Passo a Passo

1. Na lista de veículos, clique no botão **"🗑️ Excluir"**

2. **Um modal de confirmação aparece**:
   - Mostra os dados do veículo
   - ⚠️ Aviso: Todas as manutenções serão deletadas também

3. **Confirme a exclusão**:
   - Clique em **"Sim, excluir"** para confirmar
   - Ou **"Cancelar"** para desistir

4. **Aguarde a confirmação**:
   - ✅ "Veículo deletado com sucesso!"
   - A lista é atualizada automaticamente

---

## 🔧 Registrando Manutenções

### Cadastrar Nova Manutenção

#### Passo a Passo

1. No **Dashboard**, clique em **"Registrar Manutenção"**
   - Ou no menu lateral: **Manutenção → Nova Manutenção**

2. **Preencha o formulário**:
   - **Veículo:** Selecione da lista
   - **Data:** Data da manutenção
   - **Quilometragem:** KM no momento da manutenção
   - **Tipo:** Ex: Troca de óleo, Revisão, Alinhamento
   - **Prestador:** Ex: Oficina XYZ, Mecânico João
   - **Custo:** Valor em reais (ex: 150.50)
   - **Observações:** (Opcional) Detalhes adicionais

3. **Clique em "Salvar"**

4. **Aguarde a confirmação**:
   - ✅ "Manutenção registrada com sucesso!"
   - Você será redirecionado para o relatório

#### Validações

- ❌ **Data:** Não pode ser futura
- ❌ **KM:** Deve ser maior ou igual ao KM atual do veículo
- ❌ **Custo:** Deve ser um número positivo

---

### Editar Manutenção

#### Passo a Passo

1. No **Relatório de Manutenções**, clique no botão **"✏️ Editar"**

2. **Um modal se abrirá** com os dados da manutenção

3. **Edite os campos desejados**

4. **Clique em "Salvar"**

5. **O modal fecha** e a lista é atualizada

---

### Excluir Manutenção

#### Passo a Passo

1. No **Relatório de Manutenções**, clique no botão **"🗑️ Excluir"**

2. **Um modal de confirmação aparece**

3. **Confirme a exclusão**:
   - Clique em **"Sim, excluir"**

4. **Aguarde a confirmação**:
   - ✅ "Manutenção deletada com sucesso!"

---

## 📊 Relatórios

### Visualizar Relatório de Manutenções

#### Passo a Passo

1. No menu lateral, clique em **"Relatório de Manutenções"**

2. **Você verá uma tabela** com todas as manutenções:
   - Placa
   - Data
   - KM
   - Tipo
   - Prestador
   - Custo
   - Ações (Editar/Excluir)

#### Filtrar por Veículo

1. Digite a placa no campo **"Filtrar por placa"**
2. Clique em **"Filtrar"**
3. Para limpar, clique em **"Limpar Filtro"**

#### Ordenar

- Clique nos **cabeçalhos da tabela** para ordenar
- Ex: Clique em "Data" para ordenar por data

---

## 💡 Dicas e Truques

### Produtividade

1. **Use o filtro** para encontrar rapidamente
2. **Registre manutenções logo após realizá-las**
3. **Inclua observações** detalhadas
4. **Atualize o KM** do veículo regularmente

### Segurança

1. **Não compartilhe** sua senha
2. **Faça logout** ao terminar
3. **Use senhas fortes**
4. **Acesse apenas** de computadores confiáveis

### Organização

1. **Nomeie tipos de manutenção** de forma padronizada
   - ✅ "Troca de óleo"
   - ❌ "oleo" ou "ÓLEO"

2. **Registre o prestador** completo
   - ✅ "Oficina Auto Center - João"
   - ❌ "João"

3. **Seja detalhista** nas observações
   - ✅ "Óleo sintético 5W30, filtro Mann, 4L"
   - ❌ "Óleo"

---

## ❓ Perguntas Frequentes

### Posso cadastrar mais de um veículo?

Sim! Não há limite de veículos no plano básico.

### Como altero minha senha?

⚠️ Funcionalidade em desenvolvimento. Entre em contato com o administrador.

### Os dados ficam salvos?

Sim! Todos os dados são salvos no banco de dados PostgreSQL.

### Posso usar no celular?

Sim! O sistema é responsivo e funciona em smartphones e tablets.

### Como exporto os dados?

⚠️ Exportação em PDF será implementada na versão 1.4.0.

### Posso usar offline?

Não. É necessária conexão com o servidor (localhost ou remoto).

### Como adiciono foto do veículo?

⚠️ Upload de fotos será implementado na versão 1.4.0.

### O sistema tem app mobile?

⚠️ App mobile está no roadmap para a versão 2.0.0.

---

## 🔧 Solução de Problemas

### Não consigo fazer login

**Problema:** "Credenciais inválidas"

**Soluções:**
1. Verifique se o email está correto
2. Verifique se a senha está correta
3. Certifique-se de que cadastrou uma conta
4. Tente redefinir a senha (contate o admin)

---

### Veículo não aparece na lista

**Soluções:**
1. Clique em "Limpar Filtro"
2. Atualize a página (F5)
3. Verifique se foi cadastrado com sucesso
4. Verifique se está logado com o usuário correto

---

### Erro ao cadastrar veículo

**Problema:** "Placa já cadastrada"

**Solução:**
- A placa já existe no sistema
- Verifique na lista de veículos
- Use a funcionalidade de edição se necessário

---

### Erro ao registrar manutenção

**Problema:** "KM deve ser maior ou igual ao KM atual do veículo"

**Solução:**
- Atualize o KM do veículo primeiro
- Ou use um KM maior na manutenção

---

### Modal não fecha

**Soluções:**
1. Clique no botão "Cancelar"
2. Pressione ESC
3. Clique fora do modal
4. Atualize a página (F5)

---

### Página não carrega

**Soluções:**
1. Verifique se o servidor está rodando
2. Verifique a URL (http://localhost:8000)
3. Tente outro navegador
4. Limpe o cache do navegador

---

## 📞 Suporte

### Precisa de ajuda?

- 🐛 [Reportar Bug](https://github.com/GuilhemeMiranda/Python_Projetos/issues)
- 💬 [Discussões](https://github.com/GuilhemeMiranda/Python_Projetos/discussions)
- 📧 Email: contato@exemplo.com

### Documentação Técnica

- [README.md](../README.md)
- [API.md](API.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Manual criado por [Guilherme Miranda](https://github.com/GuilhemeMiranda)**

**Última atualização:** Novembro 2024 - Versão 1.3.0