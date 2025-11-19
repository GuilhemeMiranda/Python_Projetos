from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app import security, models

router = APIRouter()

def _get_user_by_email(db: Session, email: str):
    """Busca usuário por email de forma segura."""
    try:
        result = db.execute(
            text("SELECT * FROM usuarios WHERE email = :email"),
            {"email": email}
        ).fetchone()
        return result
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None

def _extract_email_field(user):
    """Extrai o campo de email de diferentes formatos de usuário."""
    if user is None:
        return None
    if hasattr(user, "email"):
        return user.email
    if isinstance(user, dict):
        return user.get("email")
    if hasattr(user, "_mapping"):
        return user._mapping.get("email")
    try:
        return user[1] if len(user) > 1 else None
    except (TypeError, IndexError):
        return None

def _extract_password_field(user):
    """Extrai o campo de senha de diferentes formatos de usuário."""
    if user is None:
        return None
    if hasattr(user, "senha_hash"):
        return user.senha_hash
    if isinstance(user, dict):
        return user.get("senha_hash")
    if hasattr(user, "_mapping"):
        return user._mapping.get("senha_hash")
    try:
        return user[2] if len(user) > 2 else None
    except (TypeError, IndexError):
        return None

@router.post("/auth/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    """
    Autentica o usuário e retorna token JWT.
    """
    try:
        payload = await request.json()
    except Exception:
        try:
            form = await request.form()
            payload = dict(form)
        except Exception:
            payload = {}

    email = (payload.get("email") or payload.get("username") or "").strip()
    senha = payload.get("senha") or payload.get("password") or ""

    if not email or not senha:
        return JSONResponse(
            {"detail": "E-mail e senha são obrigatórios"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user = _get_user_by_email(db, email)
    if not user:
        return JSONResponse(
            {"detail": "E-mail ou senha inválidos"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    stored = _extract_password_field(user)
    if stored is None:
        return JSONResponse(
            {"detail": "E-mail ou senha inválidos"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    if isinstance(stored, str) and stored == senha:
        authenticated = True
    else:
        try:
            authenticated = security.verificar_senha(senha, stored)
        except Exception:
            authenticated = False

    if not authenticated:
        return JSONResponse(
            {"detail": "E-mail ou senha inválidos"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    uid = getattr(user, "id", None) or getattr(user, "pk", None) or (user.get("id") if isinstance(user, dict) else None)
    uemail = _extract_email_field(user) or email
    
    token = security.criar_token_acesso({"sub": str(uid) if uid is not None else uemail, "email": uemail})
    resp = JSONResponse({"msg": "ok", "redirect": "/ui/dashboard"})
    resp.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", path="/")
    return resp

@router.post("/auth/registro")
async def api_registro(request: Request, db: Session = Depends(get_db)):
    """
    Registra um novo usuário no sistema.
    """
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            {"detail": "Dados inválidos"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    nome = payload.get("nome", "").strip()
    email = payload.get("email", "").strip()
    senha = payload.get("senha", "")

    # Validações
    if not nome or not email or not senha:
        return JSONResponse(
            {"detail": "Todos os campos são obrigatórios"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if len(senha) < 6:
        return JSONResponse(
            {"detail": "A senha deve ter no mínimo 6 caracteres"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Verifica se o email já existe
    user_exists = _get_user_by_email(db, email)
    if user_exists:
        return JSONResponse(
            {"detail": "E-mail já cadastrado"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Cria o hash da senha
    senha_hash = security.gerar_hash_senha(senha)

    # Insere o novo usuário
    try:
        db.execute(
            text("INSERT INTO usuarios (nome, email, senha_hash) VALUES (:nome, :email, :senha_hash)"),
            {"nome": nome, "email": email, "senha_hash": senha_hash}
        )
        db.commit()

        # Busca o usuário criado
        novo_usuario = _get_user_by_email(db, email)
        uid = getattr(novo_usuario, "id", None) or (novo_usuario.get("id") if isinstance(novo_usuario, dict) else None)

        return JSONResponse(
            {"msg": "Usuário cadastrado com sucesso", "id": uid, "email": email},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar usuário: {e}")
        return JSONResponse(
            {"detail": "Erro ao cadastrar usuário"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/auth/logout")
def api_logout():
    """
    Faz logout do usuário removendo o token.
    """
    resp = RedirectResponse("/ui/login", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie("access_token", path="/")
    return resp