# Makefile para automatizar tarefas comuns do projeto

.PHONY: help install install-dev run test test-cov lint format clean build docker-up docker-down

# Variáveis
PYTHON := python3
PIP := pip3
APP_MODULE := app.main:app
PORT := 8000

# Cores para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# =================================================================
# Help - Lista todos os comandos disponíveis
# =================================================================
help:
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@echo ""
	@echo "  $(YELLOW)install$(NC)          - Instala as dependências do projeto"
	@echo "  $(YELLOW)install-dev$(NC)      - Instala dependências de desenvolvimento"
	@echo "  $(YELLOW)run$(NC)              - Executa a aplicação em modo desenvolvimento"
	@echo "  $(YELLOW)run-prod$(NC)         - Executa a aplicação em modo produção"
	@echo "  $(YELLOW)test$(NC)             - Executa os testes"
	@echo "  $(YELLOW)test-cov$(NC)         - Executa testes com relatório de cobertura"
	@echo "  $(YELLOW)lint$(NC)             - Verifica qualidade do código (flake8, mypy)"
	@echo "  $(YELLOW)format$(NC)           - Formata o código com Black"
	@echo "  $(YELLOW)format-check$(NC)     - Verifica formatação sem modificar"
	@echo "  $(YELLOW)clean$(NC)            - Remove arquivos temporários e cache"
	@echo "  $(YELLOW)clean-db$(NC)         - Remove banco de dados SQLite"
	@echo "  $(YELLOW)docker-up$(NC)        - Inicia containers Docker"
	@echo "  $(YELLOW)docker-down$(NC)      - Para containers Docker"
	@echo "  $(YELLOW)docker-logs$(NC)      - Mostra logs dos containers"
	@echo "  $(YELLOW)migrate$(NC)          - Executa migrações do banco (Alembic)"
	@echo "  $(YELLOW)setup$(NC)            - Configuração inicial completa"
	@echo ""

# =================================================================
# Instalação
# =================================================================
install:
	@echo "$(GREEN)Instalando dependências...$(NC)"
	$(PIP) install -r requirements.txt

install-dev:
	@echo "$(GREEN)Instalando dependências de desenvolvimento...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy pylint

# =================================================================
# Execução
# =================================================================
run:
	@echo "$(GREEN)Iniciando aplicação em modo desenvolvimento...$(NC)"
	uvicorn $(APP_MODULE) --reload --host 0.0.0.0 --port $(PORT)

run-prod:
	@echo "$(GREEN)Iniciando aplicação em modo produção...$(NC)"
	uvicorn $(APP_MODULE) --host 0.0.0.0 --port $(PORT) --workers 4

# =================================================================
# Testes
# =================================================================
test:
	@echo "$(GREEN)Executando testes...$(NC)"
	pytest tests/ -v

test-cov:
	@echo "$(GREEN)Executando testes com cobertura...$(NC)"
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
	@echo "$(YELLOW)Relatório HTML gerado em htmlcov/index.html$(NC)"

test-watch:
	@echo "$(GREEN)Executando testes em modo watch...$(NC)"
	pytest-watch tests/ -v

# =================================================================
# Qualidade de Código
# =================================================================
lint:
	@echo "$(GREEN)Verificando qualidade do código...$(NC)"
	@echo "$(YELLOW)Executando Flake8...$(NC)"
	flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app/ --count --max-complexity=10 --max-line-length=100 --statistics
	@echo "$(YELLOW)Executando MyPy...$(NC)"
	mypy app/ || true

format:
	@echo "$(GREEN)Formatando código com Black...$(NC)"
	black app/ tests/

format-check:
	@echo "$(GREEN)Verificando formatação...$(NC)"
	black --check app/ tests/

# =================================================================
# Limpeza
# =================================================================
clean:
	@echo "$(GREEN)Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	@echo "$(GREEN)Limpeza concluída!$(NC)"

clean-db:
	@echo "$(YELLOW)Removendo banco de dados...$(NC)"
	rm -f manutencao_veicular.db
	rm -f test_manutencao_veicular.db

# =================================================================
# Docker
# =================================================================
docker-up:
	@echo "$(GREEN)Iniciando containers Docker...$(NC)"
	docker-compose up -d

docker-down:
	@echo "$(GREEN)Parando containers Docker...$(NC)"
	docker-compose down

docker-logs:
	@echo "$(GREEN)Mostrando logs dos containers...$(NC)"
	docker-compose logs -f

docker-build:
	@echo "$(GREEN)Construindo imagem Docker...$(NC)"
	docker-compose build

# =================================================================
# Banco de Dados
# =================================================================
migrate:
	@echo "$(GREEN)Executando migrações...$(NC)"
	alembic upgrade head

migrate-create:
	@echo "$(GREEN)Criando nova migração...$(NC)"
	@read -p "Nome da migração: " msg; \
	alembic revision --autogenerate -m "$$msg"

migrate-rollback:
	@echo "$(YELLOW)Revertendo última migração...$(NC)"
	alembic downgrade -1

# =================================================================
# Configuração Inicial
# =================================================================
setup: clean install
	@echo "$(GREEN)Configuração inicial...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Criando arquivo .env...$(NC)"; \
		cp .env.example .env; \
		echo "$(RED)IMPORTANTE: Configure as variáveis no arquivo .env$(NC)"; \
	fi
	@echo "$(GREEN)Setup concluído!$(NC)"
	@echo "$(YELLOW)Execute 'make run' para iniciar a aplicação$(NC)"

# =================================================================
# Análise de Segurança
# =================================================================
security:
	@echo "$(GREEN)Verificando segurança...$(NC)"
	@echo "$(YELLOW)Verificando vulnerabilidades em dependências...$(NC)"
	safety check || true
	@echo "$(YELLOW)Analisando código para problemas de segurança...$(NC)"
	bandit -r app/ || true

# =================================================================
# Documentação
# =================================================================
docs:
	@echo "$(GREEN)Abrindo documentação da API...$(NC)"
	@echo "$(YELLOW)Swagger UI: http://localhost:$(PORT)/docs$(NC)"
	@echo "$(YELLOW)ReDoc: http://localhost:$(PORT)/redoc$(NC)"

# =================================================================
# Utilities
# =================================================================
shell:
	@echo "$(GREEN)Iniciando shell Python...$(NC)"
	$(PYTHON) -i -c "from app import models, schemas, crud, database"

.DEFAULT_GOAL := help
