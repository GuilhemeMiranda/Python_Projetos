# =================================================================
# Multi-stage Dockerfile para API de Manutenção Veicular
# =================================================================

# Stage 1: Builder
FROM python:3.10-slim as builder

WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Copiar dependências do stage builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código da aplicação
COPY --chown=appuser:appuser ./app ./app

# Configurar PATH para incluir binários do usuário
ENV PATH=/home/appuser/.local/bin:$PATH

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
