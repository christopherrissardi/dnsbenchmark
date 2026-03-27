import sqlite3
import os
from src.config import DATABASE_PATH

def _dict_factory(cursor, row):
    """Converte resultados de consulta de tuplas para dicionários."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def _get_db_connection():
    """Estabelece uma conexão com o banco de dados SQLite."""
    if not os.path.exists(DATABASE_PATH):
        print(f"Banco de dados não encontrado em '{DATABASE_PATH}'.")
        print("Por favor, execute o script 'scripts/import_json_to_sqlite.py' para criá-lo.")
        return None
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = _dict_factory
    return conn

def get_top_dns():
    """Busca a lista dos principais servidores DNS."""
    conn = _get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dns_servers WHERE is_top = 1")
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_dns_by_city(city):
    """Busca servidores DNS para uma cidade específica."""
    conn = _get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dns_servers WHERE lower(city) = ?", (city.lower(),))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_dns_by_country(country_id):
    """Busca servidores DNS para um país específico."""
    conn = _get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dns_servers WHERE country_id = ?", (country_id.upper(),))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_all_dns_counts(city, country_id):
    """Obtém a contagem de servidores DNS para top, cidade e país."""
    conn = _get_db_connection()
    if not conn:
        return 0, 0, 0
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(ip) FROM dns_servers WHERE is_top = 1")
    top_dns_count = cursor.fetchone()['COUNT(ip)']
    cursor.execute("SELECT COUNT(ip) FROM dns_servers WHERE lower(city) = ?", (city.lower(),))
    city_dns_count = cursor.fetchone()['COUNT(ip)']
    cursor.execute("SELECT COUNT(ip) FROM dns_servers WHERE country_id = ?", (country_id.upper(),))
    country_dns_count = cursor.fetchone()['COUNT(ip)']
    conn.close()
    return top_dns_count, city_dns_count, country_dns_count