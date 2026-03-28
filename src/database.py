import sqlite3
import os

# Caminho para o banco de dados
DATABASE_PATH = os.path.join("data", "DNS.db")

def _dict_factory(cursor, row):
    """Converte resultados de consulta de tuplas para dicionários."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def _get_db_connection():
    """Estabelece uma conexão com o banco de dados SQLite."""
    if not os.path.exists(DATABASE_PATH):
        return None
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = _dict_factory
    return conn

def get_top_dns():
    """Busca todos os servidores da tabela TOP_DNS (Lista de Elite)."""
    conn = _get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    # Removemos o filtro is_top, pois a tabela já é a lista correta
    cursor.execute("SELECT * FROM TOP_DNS")
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_dns_by_city(city):
    """Busca servidores para uma cidade específica dentro da sua lista curada."""
    conn = _get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TOP_DNS WHERE CITY = ?", (city.lower(),))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_dns_by_country(country_id):
    """Busca servidores para um país específico dentro da sua lista curada."""
    conn = _get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TOP_DNS WHERE COUNTRY_CODE = ?", (country_id.upper(),))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_all_dns_counts(city, country_id):
    """Obtém a contagem total da lista, por cidade e por país."""
    conn = _get_db_connection()
    if not conn:
        return 0, 0, 0
    
    cursor = conn.cursor()
    
    # Contagem Total (Tops)
    cursor.execute("SELECT COUNT(IP) AS total FROM TOP_DNS")
    top_dns_count = cursor.fetchone()['total']
    
    # Contagem Cidade
    cursor.execute("SELECT COUNT(IP) AS total FROM TOP_DNS WHERE CITY = ?", (city.lower(),))
    city_dns_count = cursor.fetchone()['total']
    
    # Contagem País
    cursor.execute("SELECT COUNT(IP) AS total FROM TOP_DNS WHERE COUNTRY_CODE = ?", (country_id.upper(),))
    country_dns_count = cursor.fetchone()['total']
    
    conn.close()
    return top_dns_count, city_dns_count, country_dns_count