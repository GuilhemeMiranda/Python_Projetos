from pathlib import Path
import runpy
import sys
from sqlalchemy import MetaData, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def try_import(modname):
    try:
        return __import__(modname, fromlist=['*'])
    except Exception:
        return None

def get_engine():
    # tenta importar engine padrão
    for modname in ("app.database", "APP.database"):
        mod = try_import(modname)
        if mod and hasattr(mod, "engine"):
            return mod.engine
    # procura arquivo DB sqlite na hierarquia
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        dbf = p / "manutencao_veicular.db"
        if dbf.exists():
            return create_engine(f"sqlite:///{dbf}", connect_args={"check_same_thread": False})
    # tenta extrair DATABASE_URL executando database.py
    for p in [here] + list(here.parents):
        for sub in ("app", "APP"):
            cand = p / sub / "database.py"
            if cand.exists():
                data = runpy.run_path(str(cand))
                url = data.get("DATABASE_URL") or data.get("database_url")
                if url:
                    return create_engine(url, connect_args={"check_same_thread": False})
    raise SystemExit("Não encontrou engine/DB. Verifique app.database ou arquivo .db")

def find_user_table(meta: MetaData):
    candidates = [t for t in meta.tables.keys() if any(k in t.lower() for k in ("usuario","usuarios","user","users"))]
    return candidates[0] if candidates else None

def find_cols(table):
    cols = [c.name for c in table.columns]
    email_col = next((c for c in cols if "email" in c.lower()), None)
    pwd_col = next((c for c in cols if any(k in c.lower() for k in ("senha","password","pwd","pass","hash"))), None)
    return email_col, pwd_col, cols

def try_security_verify(password, stored):
    sec = try_import("app.security") or try_import("APP.security")
    if not sec:
        return None, None
    # procura função comum
    for name in ("verificar_senha","verify_password","verify_password_hash","check_password"):
        fn = getattr(sec, name, None)
        if callable(fn):
            try:
                return fn(password, stored), f"usando {name}() de {sec.__name__}"
            except Exception as e:
                return False, f"erro ao chamar {name}(): {e}"
    return None, None

def try_bcrypt_verify(password, stored):
    try:
        from passlib.hash import bcrypt
        ok = bcrypt.verify(password, stored)
        return ok, "passlib.bcrypt.verify"
    except Exception as e:
        return None, f"bcrypt não aplicável: {e}"

def main(email, senha):
    engine = get_engine()
    meta = MetaData()
    try:
        meta.reflect(bind=engine)
    except SQLAlchemyError as e:
        raise SystemExit(f"Falha ao refletir metadata: {e}")
    table_name = find_user_table(meta)
    if not table_name:
        print("Tabela de usuários não encontrada. Tabelas:", ", ".join(meta.tables.keys()))
        return
    table = meta.tables[table_name]
    email_col, pwd_col, all_cols = find_cols(table)
    print(f"Usando tabela: {table_name}")
    print(f"Colunas: {all_cols}")
    print(f"Email col detectada: {email_col}, senha col detectada: {pwd_col}")

    with engine.connect() as conn:
        stmt = select(table).where(getattr(table.c, email_col) == email) if email_col else select(table)
        row = conn.execute(stmt).first()
        if not row:
            print("Usuário não encontrado para email:", email)
            return
        rowd = dict(row._mapping)
        print("Registro encontrado:", rowd)
        stored = rowd.get(pwd_col) if pwd_col else None
        print("Valor armazenado (senha):", repr(stored))

        reasons = []
        # limpeza comum
        if isinstance(stored, str):
            s_stripped = stored.strip()
        else:
            s_stripped = stored

        # teste igualdade direta
        direct = (s_stripped == senha)
        print(f"Igualdade direta senha_provide == stored? {direct}")

        # testar security module
        sec_res, sec_msg = try_security_verify(senha, stored)
        if sec_res is not None:
            print(f"Verificação security: {sec_res} ({sec_msg})")
            reasons.append(("security", sec_res, sec_msg))

        # tentar bcrypt se não testado por security
        bc_res, bc_msg = try_bcrypt_verify(senha, stored)
        if bc_res is not None:
            print(f"Verificação bcrypt: {bc_res} ({bc_msg})")
            reasons.append(("bcrypt", bc_res, bc_msg))

        # sugestoes
        if direct or any(r[1] for r in reasons):
            print("Conclusão: credenciais OK (um dos métodos validou).")
        else:
            print("Conclusão: nenhuma verificação validou.")
            print("Sugestões:")
            print("- Confirme que o email/math exato no DB é igual (case sensitive depende da consulta).")
            print("- Verifique se a senha no DB está armazenada como hash com outro algoritmo.")
            print("- Cole aqui o valor armazenado da senha (só em ambiente seguro) para eu ajudar a identificar o formato.")
            print("- Se armazenar em texto simples, verifique espaços/encoding.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python check_login_local.py email senha")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])