import argparse
import json
import runpy
from pathlib import Path
from sqlalchemy import MetaData, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def get_engine():
    # tenta importar engines padrões
    try:
        from app.database import engine as eng
        return eng
    except Exception:
        pass
    try:
        from APP.database import engine as eng
        return eng
    except Exception:
        pass

    # procura arquivo manutencao_veicular.db em hierarquia de pastas a partir deste script
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        db_file = p / "manutencao_veicular.db"
        if db_file.exists():
            url = f"sqlite:///{db_file}"
            return create_engine(url, connect_args={"check_same_thread": False})

    # procura por APP/database.py ou app/database.py e executa para extrair DATABASE_URL
    for p in [here] + list(here.parents):
        candidate = p / "APP" / "database.py"
        if candidate.exists():
            data = runpy.run_path(str(candidate))
            url = data.get("DATABASE_URL") or data.get("database_url")
            if url:
                return create_engine(url, connect_args={"check_same_thread": False})
        candidate2 = p / "app" / "database.py"
        if candidate2.exists():
            data = runpy.run_path(str(candidate2))
            url = data.get("DATABASE_URL") or data.get("database_url")
            if url:
                return create_engine(url, connect_args={"check_same_thread": False})

    raise RuntimeError("Não foi possível localizar a engine ou o arquivo de banco (APP/database.py ou manutencao_veicular.db).")

def find_user_table(metadata: MetaData):
    # procura tabelas com nomes relacionados a usuário
    candidates = [t for t in metadata.tables.keys() if any(k in t.lower() for k in ("usuario", "usuarios", "user", "users"))]
    if candidates:
        return candidates[0]
    return None

def main():
    try:
        engine = get_engine()
    except Exception as e:
        raise SystemExit(f"Erro ao obter engine do projeto: {e}")

    meta = MetaData()
    try:
        meta.reflect(bind=engine)
    except SQLAlchemyError as e:
        raise SystemExit(f"Falha ao refletir metadata: {e}")

    table_name = find_user_table(meta)
    if not table_name:
        print("Não foi possível localizar automaticamente a tabela de usuários.")
        print("Tabelas encontradas:", ", ".join(meta.tables.keys()))
        return

    table = meta.tables[table_name]
    print(f"Usando tabela: {table_name}")
    cols = [c.name for c in table.columns]
    # identifica possíveis colunas de senha
    pwd_cols = [c for c in cols if any(k in c.lower() for k in ("senha", "password", "pwd", "pass", "hash"))]
    if not pwd_cols:
        print("Nenhuma coluna de senha identificada automaticamente. Colunas disponíveis:", cols)
        # ainda assim mostra todas as colunas
    with engine.connect() as conn:
        stmt = select(table)
        rows = conn.execute(stmt).fetchall()

    output = []
    for row in rows:
        rowd = dict(row._mapping)
        # MOSTRA senha completa por design (cuidado)
        for pc in pwd_cols:
            val = rowd.get(pc)
            if val is None:
                continue
            rowd[pc] = val  # sem mascaramento
        output.append(rowd)

    # imprime em JSON legível
    print(json.dumps({"table": table_name, "password_columns": pwd_cols, "count": len(output), "rows": output}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    # execução direta sempre mostra as senhas completas (use apenas localmente)
    main()