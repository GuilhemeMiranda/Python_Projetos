"""
Script para descobrir DEFINITIVAMENTE qual banco está sendo usado
"""
import os
from pathlib import Path

print("=" * 80)
print("🔍 DESCOBRINDO QUAL BANCO DE DADOS ESTÁ SENDO USADO")
print("=" * 80)

# 1. Verificar database.py
print("\n📂 ETAPA 1: Verificando database.py")
print("-" * 80)

database_path = Path("app/database.py")
if database_path.exists():
    with open(database_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("Conteúdo do database.py:")
    print("-" * 80)
    print(content)
    print("-" * 80)
    
    if "sqlite" in content.lower():
        print("\n✅ ENCONTRADO: Referência ao SQLite")
    if "postgresql" in content.lower() or "postgres" in content.lower():
        print("\n✅ ENCONTRADO: Referência ao PostgreSQL")
else:
    print("❌ Arquivo database.py não encontrado!")

# 2. Verificar arquivos de banco
print("\n📂 ETAPA 2: Procurando arquivos de banco")
print("-" * 80)

# Procurar arquivos SQLite
sqlite_files = list(Path(".").glob("*.db")) + list(Path(".").glob("*.sqlite"))
if sqlite_files:
    print("\n✅ ARQUIVOS SQLite ENCONTRADOS:")
    for file in sqlite_files:
        size = file.stat().st_size
        print(f"   📦 {file.name} ({size:,} bytes)")
else:
    print("\n⚠️  Nenhum arquivo .db ou .sqlite encontrado")

# 3. Verificar variáveis de ambiente
print("\n📂 ETAPA 3: Verificando variáveis de ambiente")
print("-" * 80)

db_url = os.environ.get("DATABASE_URL")
if db_url:
    print(f"✅ DATABASE_URL encontrada: {db_url}")
else:
    print("⚠️  Variável DATABASE_URL não definida")

# 4. Tentar importar e verificar
print("\n📂 ETAPA 4: Tentando importar e verificar engine")
print("-" * 80)

try:
    from app.database import engine, SQLALCHEMY_DATABASE_URL
    
    print(f"✅ URL de Conexão:")
    print(f"   {SQLALCHEMY_DATABASE_URL}")
    
    print(f"\n✅ Tipo do Dialect:")
    print(f"   {engine.dialect.name}")
    
    print(f"\n✅ Driver:")
    print(f"   {engine.driver}")
    
    print(f"\n✅ Classe do Dialect:")
    print(f"   {type(engine.dialect).__name__}")
    
    # CONCLUSÃO
    print("\n" + "=" * 80)
    print("🎯 CONCLUSÃO")
    print("=" * 80)
    
    if engine.dialect.name == 'sqlite':
        print("\n✅✅✅ VOCÊ ESTÁ USANDO: SQLite")
        print("\n📝 Características:")
        print("   • Banco de dados em arquivo (.db)")
        print("   • Sem servidor separado")
        print("   • Ideal para desenvolvimento")
        
        # Verificar se o arquivo existe
        db_file = SQLALCHEMY_DATABASE_URL.replace('sqlite:///', '')
        if os.path.exists(db_file):
            print(f"\n📦 Arquivo do banco: {db_file}")
            print(f"   Tamanho: {os.path.getsize(db_file):,} bytes")
        else:
            print(f"\n⚠️  Arquivo do banco NÃO existe ainda: {db_file}")
            print("   (Será criado automaticamente no primeiro acesso)")
    
    elif engine.dialect.name == 'postgresql':
        print("\n✅✅✅ VOCÊ ESTÁ USANDO: PostgreSQL")
        print("\n📝 Características:")
        print("   • Banco de dados em servidor")
        print("   • Requer instalação do PostgreSQL")
        print("   • Ideal para produção")
        print("\n⚠️  IMPORTANTE: Use os scripts SQL do PostgreSQL!")
    
    else:
        print(f"\n❓ VOCÊ ESTÁ USANDO: {engine.dialect.name.upper()}")
    
    print("=" * 80)
    
    # Testar conexão
    print("\n🔌 ETAPA 5: Testando conexão")
    print("-" * 80)
    
    try:
        with engine.connect() as conn:
            if engine.dialect.name == 'sqlite':
                result = conn.execute("SELECT sqlite_version()")
                version = result.fetchone()[0]
                print(f"✅ Conexão OK! SQLite versão: {version}")
            elif engine.dialect.name == 'postgresql':
                result = conn.execute("SELECT version()")
                version = result.fetchone()[0]
                print(f"✅ Conexão OK! PostgreSQL versão: {version}")
            else:
                conn.execute("SELECT 1")
                print("✅ Conexão OK!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
    
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

print("\n" + "=" * 80)