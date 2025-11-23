# Guia de Segurança e Boas Práticas

Este documento descreve práticas de segurança essenciais para o projeto API de Manutenção Veicular.

## 📋 Índice

1. [Segurança de Credenciais](#segurança-de-credenciais)
2. [Autenticação e Autorização](#autenticação-e-autorização)
3. [Validação de Entrada](#validação-de-entrada)
4. [Proteção contra Ataques Comuns](#proteção-contra-ataques-comuns)
5. [Configuração Segura](#configuração-segura)
6. [Auditoria e Monitoramento](#auditoria-e-monitoramento)
7. [Dependências Seguras](#dependências-seguras)
8. [Checklist de Segurança](#checklist-de-segurança)

## 🔐 Segurança de Credenciais

### ⚠️ NUNCA Commite Segredos

```python
# ❌ ERRADO - Nunca faça isso!
DATABASE_URL = "postgresql://user:senha123@localhost/db"
API_KEY = "minha-chave-secreta-123"

# ✅ CORRETO - Use variáveis de ambiente
import os
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
```

### Gerenciamento de Senhas

**Implementar hash de senhas com bcrypt:**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera hash seguro da senha."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

**Atualizar `crud.py`:**

```python
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Cria um novo usuário no banco."""
    # Hash da senha antes de salvar
    senha_hash = hash_password(usuario.senha)
    
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario
```

## 🎫 Autenticação e Autorização

### Implementar JWT (JSON Web Tokens)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verifica e decodifica token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Middleware de Autenticação

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtém usuário atual do token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # Buscar usuário no banco
    # ...
    return user
```

## ✅ Validação de Entrada

### Sempre Use Schemas Pydantic

```python
from pydantic import BaseModel, EmailStr, validator, Field

class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=100)
    
    @validator('senha')
    def senha_forte(cls, v):
        """Valida força da senha."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not any(char.isupper() for char in v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        return v
```

### Sanitização de Inputs

```python
import bleach
from html import escape

def sanitize_input(text: str) -> str:
    """Remove tags HTML e sanitiza entrada."""
    # Remove tags HTML
    clean_text = bleach.clean(text, strip=True)
    # Escapa caracteres especiais
    return escape(clean_text)
```

## 🛡️ Proteção contra Ataques Comuns

### SQL Injection

**✅ SEMPRE use ORM ou prepared statements:**

```python
# ✅ CORRETO - SQLAlchemy protege contra SQL Injection
usuario = db.query(models.Usuario).filter(
    models.Usuario.email == email
).first()

# ❌ ERRADO - Vulnerável a SQL Injection
query = f"SELECT * FROM usuarios WHERE email = '{email}'"
```

### Cross-Site Scripting (XSS)

```python
from fastapi.responses import JSONResponse

# Pydantic já sanitiza automaticamente
# Mas sempre escape outputs HTML se necessário
from html import escape

@app.get("/usuario/{id}")
def get_usuario(id: int):
    usuario = crud.get_usuario(id)
    # Se retornar HTML, escape:
    # usuario.nome = escape(usuario.nome)
    return usuario
```

### Cross-Site Request Forgery (CSRF)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Especificar origens
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/usuarios/")
@limiter.limit("5/minute")  # Máximo 5 requests por minuto
def criar_usuario(request: Request, usuario: schemas.UsuarioCreate):
    # ...
    pass
```

### Proteção contra DDoS

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["exemplo.com", "*.exemplo.com"]
)
```

## ⚙️ Configuração Segura

### Variáveis de Ambiente

**Criar arquivo `.env` (NUNCA commite!):**

```bash
# Segurança
SECRET_KEY=gere_uma_chave_aleatoria_forte_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Banco de Dados
DATABASE_URL=sqlite:///./manutencao_veicular.db

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://seuapp.com

# Ambiente
ENVIRONMENT=production
DEBUG=False
```

### Carregar Configurações

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str
    allowed_origins: list = []
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### HTTPS em Produção

```python
# Redirecionar HTTP para HTTPS
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

## 📊 Auditoria e Monitoramento

### Logging Seguro

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.post("/usuarios/")
def criar_usuario(usuario: schemas.UsuarioCreate):
    # ❌ NUNCA logue senhas ou dados sensíveis
    logger.info(f"Tentativa de criar usuário: {usuario.email}")
    
    try:
        novo_usuario = crud.criar_usuario(db, usuario)
        logger.info(f"Usuário criado com sucesso: ID {novo_usuario.id}")
        return novo_usuario
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise
```

### Monitoramento de Erros

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

if settings.environment == "production":
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0,
    )
```

## 📦 Dependências Seguras

### Verificar Vulnerabilidades

```bash
# Instalar safety
pip install safety

# Verificar vulnerabilidades
safety check

# Gerar relatório
safety check --json > security-report.json
```

### Manter Dependências Atualizadas

```bash
# Verificar atualizações
pip list --outdated

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

### Fixar Versões

```txt
# requirements.txt
fastapi==0.104.1  # Versão específica
uvicorn>=0.24.0,<0.25.0  # Range permitido
```

## ✔️ Checklist de Segurança

### Antes de Deploy em Produção

- [ ] Todas as senhas são hasheadas (bcrypt)
- [ ] JWT implementado para autenticação
- [ ] Variáveis de ambiente configuradas (.env)
- [ ] SECRET_KEY forte e aleatória
- [ ] DEBUG=False em produção
- [ ] HTTPS configurado
- [ ] CORS configurado corretamente
- [ ] Rate limiting implementado
- [ ] Validação de entrada em todos os endpoints
- [ ] SQL Injection protegido (usando ORM)
- [ ] XSS protegido (sanitização de outputs)
- [ ] Logging configurado (sem dados sensíveis)
- [ ] Dependências atualizadas e verificadas
- [ ] Backup do banco de dados configurado
- [ ] Monitoramento de erros (Sentry/similar)
- [ ] Testes de segurança executados

### Código

- [ ] Nenhum segredo commitado no repositório
- [ ] .env no .gitignore
- [ ] Código revisado por pares
- [ ] Testes de segurança automatizados

### Infraestrutura

- [ ] Firewall configurado
- [ ] Acesso SSH apenas com chave
- [ ] Atualizações de segurança automáticas
- [ ] Backup automatizado
- [ ] Certificado SSL válido

## 🔧 Ferramentas Recomendadas

### Análise de Código

```bash
# Bandit - Verifica vulnerabilidades em Python
pip install bandit
bandit -r app/

# PyLint Security
pip install pylint
pylint --load-plugins=pylint.extensions.security app/
```

### Testes de Segurança

```bash
# OWASP ZAP - Teste de penetração
# https://www.zaproxy.org/

# SQLMap - Teste SQL Injection
# http://sqlmap.org/
```

## 📚 Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)

## 🆘 Reportando Vulnerabilidades

Se você encontrar uma vulnerabilidade de segurança, **NÃO abra uma issue pública**.

Entre em contato diretamente:
- Email: security@exemplo.com
- Use GitHub Security Advisories

---

**Segurança é um processo contínuo, não uma meta única!**

**Última atualização:** Novembro 2024
