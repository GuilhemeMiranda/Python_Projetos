"""
Script para recriar as tabelas de planos com a nova estrutura
"""
import sqlite3
import os
from pathlib import Path

def encontrar_banco():
    """Encontra o banco de dados"""
    caminhos_possiveis = [
        "manutencao_veicular.db",
        "../manutencao_veicular.db",
        "Manutencao_Veicular/manutencao_veicular.db",
    ]
    
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return caminho
    
    # Procurar recursivamente
    for root, dirs, files in os.walk(".."):
        for file in files:
            if file == "manutencao_veicular.db":
                return os.path.join(root, file)
    
    return None

def recriar_tabelas():
    """Recria as tabelas de planos com a nova estrutura"""
    
    print("=" * 70)
    print("🔧 RECRIANDO TABELAS DE PLANOS")
    print("=" * 70)
    
    DB_PATH = encontrar_banco()
    
    if not DB_PATH:
        print("\n❌ Banco de dados não encontrado!")
        print("\n📂 Pasta atual:", os.getcwd())
        print("\n💡 Certifique-se de estar na pasta do projeto:")
        print("   cd Manutencao_Veicular")
        return
    
    print(f"\n✅ Banco encontrado: {DB_PATH}")
    print(f"📂 Caminho completo: {os.path.abspath(DB_PATH)}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("\n🗑️  Deletando tabelas antigas...")
        cursor.execute("DROP TABLE IF EXISTS veiculos_planos")
        cursor.execute("DROP TABLE IF EXISTS planos_manutencao")
        print("   ✓ Tabelas antigas removidas")
        
        print("\n🔨 Criando tabela planos_manutencao...")
        cursor.execute("""
            CREATE TABLE planos_manutencao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(200) NOT NULL,
                descricao TEXT,
                km_intervalo INTEGER,
                dias_intervalo INTEGER,
                usuario_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                CHECK (km_intervalo IS NULL OR km_intervalo > 0),
                CHECK (dias_intervalo IS NULL OR dias_intervalo > 0),
                CHECK (km_intervalo IS NOT NULL OR dias_intervalo IS NOT NULL)
            )
        """)
        print("   ✓ planos_manutencao criada")
        
        print("\n🔨 Criando tabela veiculos_planos...")
        cursor.execute("""
            CREATE TABLE veiculos_planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                veiculo_id INTEGER NOT NULL,
                plano_manutencao_id INTEGER NOT NULL,
                data_inicio DATE NOT NULL,
                proxima_manutencao_km INTEGER,
                proxima_manutencao_data DATE,
                ativo BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE,
                FOREIGN KEY (plano_manutencao_id) REFERENCES planos_manutencao(id) ON DELETE CASCADE,
                UNIQUE (veiculo_id, plano_manutencao_id)
            )
        """)
        print("   ✓ veiculos_planos criada")
        
        print("\n📊 Criando índices...")
        indices = [
            ("idx_planos_usuario", "planos_manutencao(usuario_id)"),
            ("idx_veiculos_planos_veiculo", "veiculos_planos(veiculo_id)"),
            ("idx_veiculos_planos_plano", "veiculos_planos(plano_manutencao_id)"),
            ("idx_veiculos_planos_ativo", "veiculos_planos(ativo)")
        ]
        
        for idx_name, idx_def in indices:
            cursor.execute(f"CREATE INDEX {idx_name} ON {idx_def}")
            print(f"   ✓ {idx_name}")
        
        conn.commit()
        
        print("\n" + "=" * 70)
        print("✅ TABELAS CRIADAS COM SUCESSO!")
        print("=" * 70)
        
        print("\n📋 Verificando tabelas criadas...")
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        for tabela in cursor.fetchall():
            print(f"   ✓ {tabela[0]}")
        
        print("\n" + "=" * 70)
        print("💡 PRÓXIMO PASSO:")
        print("   1. Reiniciar o servidor")
        print("   2. Testar as telas antigas")
        print("   3. Atualizar schemas.py")
        print("=" * 70 + "\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ ERRO: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    recriar_tabelas()