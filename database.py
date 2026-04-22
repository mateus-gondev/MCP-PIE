import sqlite3

DB_NAME = "gestao.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabela de Clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT, info TEXT, endereco TEXT)''')
    # Tabela de Produtos
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL, estoque INTEGER)''')
    conn.commit()
    conn.close()

def salvar_novo(tabela, **kwargs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    colunas = ', '.join(kwargs.keys())
    placeholders = ', '.join(['?'] * len(kwargs))
    sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
    cursor.execute(sql, list(kwargs.values()))
    conn.commit()
    conn.close()
    return f" {tabela.capitalize()} cadastrado com sucesso!"

def atualizar_registro(tabela, registro_id, **kwargs):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    sql = f"UPDATE {tabela} SET {set_clause} WHERE id = ?"
    cursor.execute(sql, list(kwargs.values()) + [registro_id])
    conn.commit()
    conn.close()
    return f" {tabela.capitalize()} ID {registro_id} atualizado!"

def deletar_registro(tabela, registro_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (registro_id,))
    conn.commit()
    conn.close()
    return f" {tabela.capitalize()} ID {registro_id} removido."

def buscar_registros(tabela, campo_filtro=None, valor_filtro=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if campo_filtro:
        cursor.execute(f"SELECT * FROM {tabela} WHERE {campo_filtro} LIKE ?", (f"%{valor_filtro}%",))
    else:
        cursor.execute(f"SELECT * FROM {tabela}")
    rows = cursor.fetchall()
    conn.close()
    return rows