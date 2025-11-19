from typing import Optional, Dict, Any
import os
from datetime import datetime, timedelta

import jwt
from passlib.hash import bcrypt

# Configurações — em produção leia SECRET_KEY de variáveis de ambiente seguras
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-por-favor-trocar")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 1 dia por padrão

def gerar_hash_senha(plain_password: str) -> str:
    return bcrypt.hash(plain_password)

def verificar_senha(plain_password: str, hashed_password: str) -> bool:
    if plain_password is None or hashed_password is None:
        return False
    try:
        return bcrypt.verify(plain_password, hashed_password)
    except Exception:
        return False

def criar_token_acesso(data: Dict[str, Any], expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # PyJWT >= 2 retorna str; se bytes, decode
    if isinstance(token, bytes):
        token = token.decode()
    return token

def verificar_token_seguro(token: Optional[str]) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None