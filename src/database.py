import sqlite3
import os

DATABASE_PATH = os.path.join("data", "DNS.db")

def _dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def _get_db_connection():
    if not os.path.exists(DATABASE_PATH):
        return None
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = _dict_factory
    return conn

def get_top_dns():
    conn = _get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TOP_DNS")
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_dns_by_city(city):
    conn = _get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VALID_SERVERS WHERE CITY = ? COLLATE NOCASE", (city,))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_dns_by_country(country_id):
    conn = _get_db_connection()
    if not conn: return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VALID_SERVERS WHERE COUNTRY_CODE = ?", (country_id.upper(),))
    servers = cursor.fetchall()
    conn.close()
    return servers

def get_all_dns_counts(city, country_id):
    conn = _get_db_connection()
    if not conn:
        return 0, 0, 0
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(IP) AS total FROM TOP_DNS")
    top_dns_count = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(IP) AS total FROM VALID_SERVERS WHERE CITY = ? COLLATE NOCASE", (city,))
    city_dns_count = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(IP) AS total FROM VALID_SERVERS WHERE COUNTRY_CODE = ?", (country_id.upper(),))
    country_dns_count = cursor.fetchone()['total']
    
    conn.close()
    return top_dns_count, city_dns_count, country_dns_count