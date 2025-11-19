import hashlib
import hmac
import json
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

# Configurações JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-por-favor-trocar")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 1 dia por padrão

def gerar_hash_senha(plain_password: str) -> str:
    """
    Gera o hash SHA256 da senha.
    """
    return hashlib.sha256(plain_password.encode()).hexdigest()

def verificar_senha(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha corresponde ao hash.
    """
    return gerar_hash_senha(plain_password) == hashed_password

def criar_token_acesso(data: dict) -> str:
    """
    Cria um token simples (base64 + HMAC).
    """
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire.timestamp()
    
    # Converte para JSON e depois base64
    payload_json = json.dumps(payload)
    payload_b64 = base64.b64encode(payload_json.encode()).decode()
    
    # Cria assinatura HMAC
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Token = payload.signature
    return f"{payload_b64}.{signature}"

def verificar_token_seguro(token: str) -> Optional[dict]:
    """
    Verifica e decodifica o token.
    """
    try:
        # Separa payload e signature
        parts = token.split('.')
        if len(parts) != 2:
            return None
        
        payload_b64, signature = parts
        
        # Verifica a assinatura
        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return None
        
        # Decodifica o payload
        payload_json = base64.b64decode(payload_b64).decode()
        payload = json.loads(payload_json)
        
        # Verifica expiração
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            return None
        
        return payload
    except Exception as e:
        print(f"Erro ao verificar token: {e}")
        return None