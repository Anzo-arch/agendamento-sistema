import csv
import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "dados")

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def exportar_clientes_csv(clientes, nome_arquivo="clientes_exportados.csv"):
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        caminho = os.path.join(DATA_DIR, nome_arquivo)
        with open(caminho, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(["id", "nome", "telefone", "email"])
            escritor.writerows(clientes)
        return True, f"Exportado para {caminho}"
    except Exception as e:
        return False, f"Erro ao exportar CSV: {str(e)}"

def importar_clientes_csv(caminho_arquivo):
    try:
        clientes = []
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                nome = linha.get("nome", "").strip()
                telefone = linha.get("telefone", "").strip()
                email = linha.get("email", "").strip()
                if nome:
                    clientes.append((nome, telefone, email))
        return True, clientes
    except Exception as e:
        return False, f"Erro ao importar CSV: {str(e)}"

def exportar_clientes_json(dados_clientes, nome_arquivo="clientes_exportados.json"):
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        caminho = os.path.join(DATA_DIR, nome_arquivo)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados_clientes, f, indent=4, ensure_ascii=False)
        return True, f"Exportado para {caminho}"
    except Exception as e:
        return False, f"Erro ao exportar JSON: {str(e)}"

def importar_clientes_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        clientes = []
        for item in dados:
            nome = item.get("nome", "").strip()
            telefone = item.get("telefone", "").strip()
            email = item.get("email", "").strip()
            if nome:
                clientes.append((nome, telefone, email))
        return True, clientes
    except Exception as e:
        return False, f"Erro ao importar JSON: {str(e)}"
