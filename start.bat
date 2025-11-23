@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM ====================================
REM Script de Inicialização
REM Sistema de Manutenção Veicular v1.3.0
REM ====================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      Sistema de Manutenção Veicular - Inicializando       ║
echo ║                      Versão 1.3.0                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Cores
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

REM ====================================
REM VERIFICAÇÕES PRÉ-INICIALIZAÇÃO
REM ====================================

echo %BLUE%→ Verificando ambiente...%RESET%
echo.

REM Verificar se ambiente virtual existe
if not exist .venv (
    echo %RED%✗ Ambiente virtual não encontrado!%RESET%
    echo.
    echo Execute primeiro: %GREEN%install.bat%RESET%
    echo.
    pause
    exit /b 1
)

REM Verificar se .env existe
if not exist .env (
    echo %YELLOW%⚠ Arquivo .env não encontrado!%RESET%
    echo.
    echo %YELLOW%Criando a partir de .env.example...%RESET%
    if exist .env.example (
        copy .env.example .env >nul
        echo %GREEN%✓ Arquivo .env criado%RESET%
        echo.
        echo %YELLOW%⚠ IMPORTANTE: Configure o .env antes de continuar!%RESET%
        echo   - DATABASE_URL com sua senha do PostgreSQL
        echo   - SECRET_KEY (gere com: python -c "import secrets; print(secrets.token_hex(32))")
        echo.
        notepad .env
        pause
    ) else (
        echo %RED%✗ .env.example não encontrado!%RESET%
        pause
        exit /b 1
    )
)

echo %GREEN%✓ Ambiente OK%RESET%
echo.

REM ====================================
REM ATIVAR AMBIENTE VIRTUAL
REM ====================================

echo %BLUE%→ Ativando ambiente virtual...%RESET%

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo %RED%✗ Erro ao ativar ambiente virtual%RESET%
    pause
    exit /b 1
)

echo %GREEN%✓ Ambiente virtual ativado%RESET%
echo.

REM ====================================
REM VERIFICAR CONEXÃO COM BANCO
REM ====================================

echo %BLUE%→ Verificando conexão com banco de dados...%RESET%

REM Extrair dados do DATABASE_URL do .env
for /f "tokens=2 delims==" %%a in ('findstr /C:"DATABASE_URL" .env') do set DATABASE_URL=%%a

if "!DATABASE_URL!"=="" (
    echo %RED%✗ DATABASE_URL não configurada no .env%RESET%
    pause
    exit /b 1
)

REM Verificar se PostgreSQL está rodando
pg_isready >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%⚠ PostgreSQL pode não estar rodando%RESET%
    echo.
    echo Tentando iniciar o serviço...
    net start postgresql-x64-13 >nul 2>&1
    
    timeout /t 3 >nul
    
    pg_isready >nul 2>&1
    if %errorlevel% neq 0 (
        echo %RED%✗ Não foi possível conectar ao PostgreSQL%RESET%
        echo.
        echo Verifique se o PostgreSQL está instalado e rodando:
        echo   - Abra "Serviços" do Windows
        echo   - Procure por "postgresql"
        echo   - Inicie o serviço se estiver parado
        echo.
        pause
        exit /b 1
    )
)

echo %GREEN%✓ Conexão com banco de dados OK%RESET%
echo.

REM ====================================
REM VERIFICAR PORTA 8000
REM ====================================

echo %BLUE%→ Verificando porta 8000...%RESET%

netstat -an | findstr ":8000" >nul
if %errorlevel% equ 0 (
    echo %YELLOW%⚠ Porta 8000 já está em uso!%RESET%
    echo.
    echo Deseja:
    echo   1) Matar o processo e continuar
    echo   2) Usar outra porta (8001)
    echo   3) Cancelar
    echo.
    set /p "CHOICE=Escolha (1/2/3): "
    
    if "!CHOICE!"=="1" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
            taskkill /PID %%a /F >nul 2>&1
        )
        echo %GREEN%✓ Porta 8000 liberada%RESET%
        set PORT=8000
    ) else if "!CHOICE!"=="2" (
        set PORT=8001
        echo %GREEN%✓ Usando porta 8001%RESET%
    ) else (
        echo %YELLOW%→ Operação cancelada%RESET%
        pause
        exit /b 0
    )
) else (
    set PORT=8000
    echo %GREEN%✓ Porta 8000 disponível%RESET%
)
echo.

REM ====================================
REM INICIAR SERVIDOR
REM ====================================

echo ╔════════════════════════════════════════════════════════════╗
echo ║                   INICIANDO SERVIDOR                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo %GREEN%Sistema iniciado com sucesso!%RESET%
echo.
echo %BLUE%Acesse:%RESET%
echo   • Interface:  %GREEN%http://localhost:%PORT%/ui/login%RESET%
echo   • Dashboard:  %GREEN%http://localhost:%PORT%/ui/%RESET%
echo   • API Docs:   %GREEN%http://localhost:%PORT%/docs%RESET%
echo   • ReDoc:      %GREEN%http://localhost:%PORT%/redoc%RESET%
echo.
echo %YELLOW%Pressione Ctrl+C para parar o servidor%RESET%
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Iniciar servidor
python -m uvicorn app.main:app --reload --port %PORT% --host 0.0.0.0

REM Se chegou aqui, o servidor foi parado
echo.
echo %YELLOW%→ Servidor encerrado%RESET%
echo.
pause