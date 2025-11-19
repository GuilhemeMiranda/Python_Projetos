import sys
from pathlib import Path
import runpy
from sqlalchemy import MetaData, select, create_engine

def try_import(name):
    try:
        mod = __import__(name, fromlist=['*'])
        return mod
    except Exception:
        return None

def get_engine():
    # tenta importar engine dos paquetes comuns
    mod = try_import("app.database") or try_import("APP.database")
    if mod and hasattr(mod, "engine"):
        return mod.engine
    # tenta localizar arquivo DB
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        db = p / "manutencao_veicular.db"
        if db.exists():
            return create_engine(f"sqlite:///{db}", connect_args={"check_same_thread": False})
    # tenta extrair DATABASE_URL executando database.py
    for p in [here] + list(here.parents):
        for sub in ("app", "APP"):
            cand = p / sub / "database.py"
            if cand.exists():
                data = runpy.run_path(str(cand))
                url = data.get("DATABASE_URL") or data.get("database_url")
                if url:
                    return create_engine(url, connect_args={"check_same_thread": False})
    raise SystemExit("Não encontrou engine/DB. Ajuste caminhos.")

def find_table_and_cols(meta):
    # procura tabela de usuários e colunas email/senha
    candidates = [t for t in meta.tables.keys() if any(k in t.lower() for k in ("usuario","usuarios","user","users"))]
    if not candidates:
        return None, None, None
    table = meta.tables[candidates[0]]
    cols = [c.name for c in table.columns]
    email_col = next((c for c in cols if "email" in c.lower()), None)
    pwd_col = next((c for c in cols if any(k in c.lower() for k in ("senha","password","pwd","pass","hash"))), None)
    return table, email_col, pwd_col

def main(email, senha):
    engine = get_engine()
    meta = MetaData()
    meta.reflect(bind=engine)
    table, email_col, pwd_col = find_table_and_cols(meta)
    if not table:
        print("Não encontrou tabela de usuários. Tabelas:", ", ".join(meta.tables.keys()))
        return
    if not email_col:
        print("Não encontrou coluna de email nas colunas:", [c.name for c in table.columns])
        return
    if not pwd_col:
        print("Não identificou coluna de senha automaticamente; colunas:", [c.name for c in table.columns])
        # ainda assim prossegue mostrando todas as colunas

    with engine.connect() as conn:
        stmt = select(table).where(getattr(table.c, email_col) == email)
        row = conn.execute(stmt).first()
        if not row:
            print("Usuário não encontrado para email:", email)
            return
        rowd = dict(row._mapping)
        print("Registro do usuário:", rowd)
        stored = rowd.get(pwd_col) if pwd_col else None
        print(f"Coluna senha identificada: {pwd_col} -> valor armazenado: {stored!r}")

    # tentar importar função de verificação de senha
    sec = try_import("app.security") or try_import("APP.security")
    if not sec:
        print("Módulo de segurança não encontrado (app/security.py ou APP/security.py). Não foi possível validar o hash.")
        return
    # tenta funções comuns
    verifica = None
    for name in ("verificar_senha","verify_password","verify_password_hash","check_password"):
        if hasattr(sec, name):
            verifica = getattr(sec, name)
            break
    if not verifica:
        print("Não achei função de verificação de senha no módulo security. Funções disponíveis:", [a for a in dir(sec) if "pass" in a.lower() or "verif" in a.lower()][:20])
        return
    ok = verifica(senha, stored)
    print("Resultado da verificação (senha fornecida corresponde ao armazenado?):", ok)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python debug_auth.py email senha")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])