import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "agendamento.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                servico TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

# ----- CLIENTES -----
def inserir_cliente(nome, telefone, email):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone, email))
        conn.commit()
        return cursor.lastrowid

def listar_clientes():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, telefone, email FROM clientes ORDER BY nome")
        return cursor.fetchall()

def atualizar_cliente(id_cliente, nome, telefone, email):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET nome=?, telefone=?, email=? WHERE id=?", (nome, telefone, email, id_cliente))
        conn.commit()

def deletar_cliente(id_cliente):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
        conn.commit()

# ----- AGENDAMENTOS -----
def inserir_agendamento(cliente_id, data, hora, servico):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO agendamentos (cliente_id, data, hora, servico) VALUES (?, ?, ?, ?)", (cliente_id, data, hora, servico))
        conn.commit()
        return cursor.lastrowid

def listar_agendamentos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, c.nome, a.data, a.hora, a.servico
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            ORDER BY a.data, a.hora
        """)
        return cursor.fetchall()

def buscar_agendamentos_por_cliente(cliente_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, data, hora, servico
            FROM agendamentos
            WHERE cliente_id = ?
            ORDER BY data, hora
        """, (cliente_id,))
        return cursor.fetchall()

def deletar_agendamento(agendamento_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
        conn.commit()
