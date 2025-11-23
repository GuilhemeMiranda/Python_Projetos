@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM ====================================
REM Script de Instalação Automatizada
REM Sistema de Manutenção Veicular v1.3.0
REM ====================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Sistema de Manutenção Veicular - Instalação Automática  ║
echo ║                      Versão 1.3.0                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Cores (Windows 10+)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

REM ====================================
REM PASSO 1: Verificar Python
REM ====================================
echo %BLUE%[1/8]%RESET% Verificando Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%✗ Python não encontrado!%RESET%
    echo.
    echo Por favor, instale Python 3.9+ em: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%✓ Python %PYTHON_VERSION% encontrado%RESET%
echo.

REM ====================================
REM PASSO 2: Verificar PostgreSQL
REM ====================================
echo %BLUE%[2/8]%RESET% Verificando PostgreSQL...

psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%⚠ PostgreSQL não encontrado no PATH%RESET%
    echo.
    echo Por favor, instale PostgreSQL 13+ em:
    echo https://www.postgresql.org/download/windows/
    echo.
    echo Após instalar, adicione ao PATH:
    echo C:\Program Files\PostgreSQL\13\bin
    echo.
    pause
    exit /b 1
)

for /f "tokens=3" %%i in ('psql --version') do set PSQL_VERSION=%%i
echo %GREEN%✓ PostgreSQL %PSQL_VERSION% encontrado%RESET%
echo.

REM ====================================
REM PASSO 3: Criar Ambiente Virtual
REM ====================================
echo %BLUE%[3/8]%RESET% Criando ambiente virtual...

if exist .venv (
    echo %YELLOW%⚠ Ambiente virtual já existe%RESET%
    echo.
    set /p "RECREATE=Deseja recriar? (s/n): "
    if /i "!RECREATE!"=="s" (
        echo Removendo ambiente antigo...
        rmdir /s /q .venv
        python -m venv .venv
        echo %GREEN%✓ Ambiente virtual recriado%RESET%
    ) else (
        echo %YELLOW%→ Usando ambiente existente%RESET%
    )
) else (
    python -m venv .venv
    echo %GREEN%✓ Ambiente virtual criado%RESET%
)
echo.

REM ====================================
REM PASSO 4: Ativar Ambiente Virtual
REM ====================================
echo %BLUE%[4/8]%RESET% Ativando ambiente virtual...

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo %RED%✗ Erro ao ativar ambiente virtual%RESET%
    pause
    exit /b 1
)

echo %GREEN%✓ Ambiente virtual ativado%RESET%
echo.

REM ====================================
REM PASSO 5: Atualizar pip
REM ====================================
echo %BLUE%[5/8]%RESET% Atualizando pip...

python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo %RED%✗ Erro ao atualizar pip%RESET%
    pause
    exit /b 1
)

echo %GREEN%✓ pip atualizado%RESET%
echo.

REM ====================================
REM PASSO 6: Instalar Dependências
REM ====================================
echo %BLUE%[6/8]%RESET% Instalando dependências...
echo %YELLOW%→ Isso pode demorar alguns minutos...%RESET%
echo.

pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo %RED%✗ Erro ao instalar dependências%RESET%
    echo.
    echo Tentando novamente sem --quiet para ver erros...
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo %GREEN%✓ Todas as dependências instaladas%RESET%
echo.

REM ====================================
REM PASSO 7: Configurar .env
REM ====================================
echo %BLUE%[7/8]%RESET% Configurando arquivo .env...

if exist .env (
    echo %YELLOW%⚠ Arquivo .env já existe%RESET%
    echo.
    set /p "OVERWRITE=Deseja sobrescrever? (s/n): "
    if /i "!OVERWRITE!"=="s" (
        copy /y .env.example .env >nul
        echo %GREEN%✓ Arquivo .env recriado%RESET%
    ) else (
        echo %YELLOW%→ Mantendo .env existente%RESET%
    )
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo %GREEN%✓ Arquivo .env criado%RESET%
    ) else (
        echo %RED%✗ .env.example não encontrado%RESET%
    )
)
echo.

REM ====================================
REM PASSO 8: Verificar Banco de Dados
REM ====================================
echo %BLUE%[8/8]%RESET% Verificando banco de dados...
echo.

echo %YELLOW%→ Verificando se o banco 'manutencao_veicular' existe...%RESET%

REM Solicitar senha do PostgreSQL
set /p "PGPASSWORD=Digite a senha do PostgreSQL (usuário postgres): "
echo.

REM Verificar se o banco existe
psql -U postgres -lqt 2>nul | findstr /C:"manutencao_veicular" >nul
if %errorlevel% neq 0 (
    echo %YELLOW%→ Banco não encontrado. Criando...%RESET%
    
    REM Criar banco de dados
    psql -U postgres -c "CREATE DATABASE manutencao_veicular;" 2>nul
    if %errorlevel% neq 0 (
        echo %RED%✗ Erro ao criar banco de dados%RESET%
        echo.
        echo Execute manualmente:
        echo   psql -U postgres
        echo   CREATE DATABASE manutencao_veicular;
        echo.
        pause
        exit /b 1
    )
    
    echo %GREEN%✓ Banco de dados criado%RESET%
) else (
    echo %GREEN%✓ Banco de dados já existe%RESET%
)
echo.

REM ====================================
REM CONCLUSÃO
REM ====================================
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO!          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo %GREEN%Próximos passos:%RESET%
echo.
echo %YELLOW%1.%RESET% Configure o arquivo .env:
echo    - Edite DATABASE_URL com sua senha do PostgreSQL
echo    - Gere uma SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
echo.
echo %YELLOW%2.%RESET% Inicie o servidor:
echo    - Execute: %GREEN%start.bat%RESET%
echo    - Ou: %GREEN%uvicorn app.main:app --reload%RESET%
echo.
echo %YELLOW%3.%RESET% Acesse o sistema:
echo    - Interface: %BLUE%http://localhost:8000/ui/login%RESET%
echo    - API Docs:  %BLUE%http://localhost:8000/docs%RESET%
echo.
echo %YELLOW%4.%RESET% Leia a documentação:
echo    - README.md
echo    - INSTALL.md
echo    - docs/MANUAL_USUARIO.md
echo.
echo ════════════════════════════════════════════════════════════
echo.

pause