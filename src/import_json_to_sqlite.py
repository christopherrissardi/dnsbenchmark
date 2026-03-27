import sqlite3
import json
import os
import glob

def create_database(db_path, json_folder_path):
    """
    Cria e popula um banco de dados SQLite a partir de arquivos JSON.
    """
    if os.path.exists(db_path):
        print(f"Banco de dados '{db_path}' já existe. Removendo para recriar.")
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Cria a tabela
    cursor.execute('''
    CREATE TABLE dns_servers (
        ip TEXT PRIMARY KEY,
        name TEXT,
        isp TEXT,
        city TEXT,
        country_id TEXT,
        is_top BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    print("Tabela 'dns_servers' criada.")

    # Processa os arquivos JSON
    json_files = glob.glob(os.path.join(json_folder_path, '*.json'))
    total_servers = 0

    for json_file in json_files:
        filename = os.path.basename(json_file)
        is_top = (filename == 'top_dns.json')
        
        print(f"Processando '{filename}'...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"  - Erro ao decodificar JSON de {filename}: {e}")
                continue

        for server in data:
            ip = server.get('ip')
            if not ip:
                continue

            cursor.execute("SELECT ip FROM dns_servers WHERE ip = ?", (ip,))
            if cursor.fetchone():
                continue

            cursor.execute('''
            INSERT INTO dns_servers (ip, name, isp, city, country_id, is_top)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (ip, server.get('name'), server.get('isp'), server.get('city'), server.get('country_id'), is_top))
            total_servers += 1

    conn.commit()
    conn.close()

    print(f"\nBanco de dados '{db_path}' criado com sucesso.")
    print(f"Total de servidores únicos inseridos: {total_servers}")

if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_data_path = os.path.join(project_root, 'data_json')
    db_folder_path = os.path.join(project_root, 'data')
    db_file_path = os.path.join(db_folder_path, 'dns_servers.db')

    if not os.path.exists(json_data_path):
        print(f"Erro: Pasta de dados JSON não encontrada em '{json_data_path}'")
        print("Por favor, crie-a e coloque seus arquivos .json dentro.")
    else:
        os.makedirs(db_folder_path, exist_ok=True)
        create_database(db_file_path, json_data_path)