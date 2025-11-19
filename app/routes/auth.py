from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi import Body, Form
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Any, Dict

from app.database import get_db

from app import security, crud

router = APIRouter()
# rota de UI login (se já existir em templates)
@router.get("/ui/login", include_in_schema=False)
def ui_login(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("login.html", {"request": request})

def _get_user_by_email(db: Session, email: str) -> Optional[Any]:
    # tenta várias funções comuns no crud para recuperar usuário por email
    candidates = [
        "authenticate_user",
        "get_usuario_por_email",
        "get_user_by_email",
        "get_usuario",
        "get_user",
        "find_user_by_email",
    ]
    for name in candidates:
        fn = getattr(crud, name, None)
        if callable(fn):
            try:
                # algumas funções exigem apenas (db, email)
                res = fn(db, email=email) if "email" in fn.__code__.co_varnames else fn(db, email)
                if res:
                    return res
            except Exception:
                continue

    # fallback: tenta consulta genérica via crud.list / get all e filtra
    if hasattr(crud, "get_usuarios"):
        try:
            users = crud.get_usuarios(db=db, skip=0, limit=1000)
            for u in users:
                em = getattr(u, "email", None) or (u.get("email") if isinstance(u, dict) else None)
                if em and em.lower() == email.lower():
                    return u
        except Exception:
            pass

    # fallback final: consulta direta SQL na tabela 'usuarios' (caso crud não esteja disponível)
    try:
        if db is not None:
            stmt = text("SELECT * FROM usuarios WHERE lower(email)=lower(:email) LIMIT 1")
            res = db.execute(stmt, {"email": email}).mappings().first()
            if res:
                # retorna um dict-like para o restante do código funcionar
                return dict(res)
    except Exception:
        pass

    return None

def _extract_password_field(user: Any) -> Optional[str]:
    # tenta várias propriedades possíveis onde a senha pode estar armazenada
    keys = ["senha_hash", "senha", "password_hash", "password", "pwd", "hash"]
    if user is None:
        return None
    # se for dict-like
    if isinstance(user, dict):
        for k in keys:
            if k in user and user[k] is not None:
                return user[k]
        # aliases
        for k in user.keys():
            kl = k.lower()
            if any(x in kl for x in ("senha","pass","pwd","hash")):
                return user[k]
        return None
    # objeto SQLAlchemy / model
    for k in keys:
        if hasattr(user, k):
            val = getattr(user, k)
            if val is not None:
                return val
    # tentar inspecionar todos attrs
    for attr in dir(user):
        la = attr.lower()
        if any(x in la for x in ("senha","password","pwd","hash")):
            try:
                val = getattr(user, attr)
                if not callable(val) and val is not None:
                    return val
            except Exception:
                continue
    return None

def _extract_email_field(user: Any) -> Optional[str]:
    if user is None:
        return None
    if isinstance(user, dict):
        return user.get("email") or user.get("Email")
    for attr in ("email", "Email"):
        if hasattr(user, attr):
            try:
                return getattr(user, attr)
            except Exception:
                continue
    # fallback inspect
    for attr in dir(user):
        if "email" in attr.lower():
            try:
                val = getattr(user, attr)
                if isinstance(val, str):
                    return val
            except Exception:
                continue
    return None

@router.post("/auth/login")
async def api_login(request: Request, db: Session = Depends(get_db)):
    """
    Lê o corpo diretamente (aceita JSON puro) e autentica.
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
        return JSONResponse({"detail": "email e senha são obrigatórios"}, status_code=status.HTTP_400_BAD_REQUEST)

    user = _get_user_by_email(db, email)
    if not user:
        return JSONResponse({"detail": "credenciais inválidas"}, status_code=status.HTTP_401_UNAUTHORIZED)

    stored = _extract_password_field(user)
    if stored is None:
        return JSONResponse({"detail": "credenciais inválidas"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if isinstance(stored, str) and stored == senha:
        authenticated = True
    else:
        try:
            authenticated = security.verificar_senha(senha, stored)
        except Exception:
            authenticated = False

    if not authenticated:
        return JSONResponse({"detail": "credenciais inválidas"}, status_code=status.HTTP_401_UNAUTHORIZED)

    uid = getattr(user, "id", None) or getattr(user, "pk", None) or (user.get("id") if isinstance(user, dict) else None)
    uemail = _extract_email_field(user) or email
    token = security.criar_token_acesso({"sub": str(uid) if uid is not None else uemail, "email": uemail})
    resp = JSONResponse({"msg": "ok", "redirect": "/ui/dashboard"})  # Adiciona redirect
    resp.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", path="/")
    return resp

@router.get("/auth/logout", include_in_schema=False)
def api_logout_get():
    """
    Logout via GET: remove cookie e redireciona para a tela de login.
    Compatível com navegação por window.location.href.
    """
    resp = RedirectResponse(url="/ui/login", status_code=302)
    resp.delete_cookie("access_token", path="/")
    return resp

@router.post("/auth/logout")
def api_logout():
    # retorna JSON e remove cookie com path="/"
    resp = JSONResponse({"msg": "logout"})
    resp.delete_cookie("access_token", path="/")
    return resp