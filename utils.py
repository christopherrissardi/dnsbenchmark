import os
import requests
import socket
import json

def carregar_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar JSON {caminho_arquivo}: {e}")
        return None

def main_banner(): #<------- Main Banner
    
    print(rf"""{B}                                    
{O}        ____ _       _           _  {B} ____  _   _  ____
{O}       / ___| | ___ | |__   __ _| | {B}|  _ \| \ | |/ ___|
{O}      | |  _| |/ _ \| '_ \ / _` | | {B}| | | |  \| |\___ \                                
{O}      | |_| | | (_) | |_) | (_| | | {B}| |_| | |\  | ___) |          
{O}       \____|_|\___/|_.__/ \__,_|_| {B}|____/|_| \_||____/             
{O}          {H}   ____                  _                           _            
{O}          {H}  | __ )  ___ _ __   ___| |__   _ __ ___   __ _ _ __| | __    
{O}          {H}  |  _ \ / _ | '_ \ / __| '_ \ | '_ ` _ \ / _` | '__| |/ /
{O}          {H}  | |_) |  __| | | | (__| | | || | | | | | (_| | |  |   <      
{O}          {H}  |____/ \___|_| |_|\___|_| |_||_| |_| |_|\__,_|_|  |_|\_\   
{O}                                                  
{O}                                                 Created By {B}Christopher Rissardi{O}                                                       
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

def data_information(): #<-------- Get usar information
    url = "https://ipwho.is/"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("success", False):
            print(f"""\nHello {B}{get_username()}{O}! Your Informations:    
    
[{B}+{O}] IP Address: {B}{data['ip']}{O} | Local IP Address: {B}{get_local_ip()}{O}
[{B}+{O}] City: {data['city']}, {data['region_code']}  
[{B}+{O}] Region: {data['region']} 
[{B}+{O}] Country: {data['country']} ({data['country_code']})                                      
[{B}+{O}] Continent: {data['continent']} ({data['continent_code']})                                                                     
[{B}+{O}] ISP: {data['connection']['isp']}
[{B}+{O}] Domain: {data['connection']['domain']}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

            return data
        else:
            print("Error getting external IP information. Check an API.")
            return None
    
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return None

def get_local_ip(): #<----------Get Local Host
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = 'Unavailable'
    finally:
        s.close()
    return ip_local

dados_usuario = data_information()  # <---> Information of IP Address on information.py

def get_username(): #<--------- Get username
    return os.getlogin()

def information():
    print(f"\n\nRoot Servers Available - Info")
    print("Here is the tab dedicated to information about Root-Servers spread all over the world")
    print(f"""

""")




A = "\033[0;30m" # Black/Preto               ||
B = "\033[0;31m" # Red/Vermelho              ||
C = "\033[0;32m" # Green/Verde               ||
D = "\033[0;33m" # Brown/Marrom              ||
E = "\033[0;34m" # Blue/Azul                 ||
F = "\033[0;35m" # Purple/Roxo               ||
G = "\033[0;36m" # Cyan/Ciano                ||
H = "\033[1;30m" # Black 2/Preto 2           ||
I = "\033[1;31m" # Light Red/Vermelho Claro  || 
J = "\033[1;32m" # Light Green/Verde Claro   ||  <-------- Colors
K = "\033[1;33m" # Light Yellow/Amarelo Claro||
L = "\033[1;34m" # Light Blue/Azul Claro     ||
M = "\033[1;35m" # Light Purple/Roxo Claro   ||
N = "\033[1;36m" # Light Cyan/Ciano Claro    ||
O = "\033[1;37m" # White                     ||
P = "\033[4;30m" # Underline/Sublinhado      ||
Q = "\033[5;30m" # Blinking/Piscando         ||
R = "\033[7;30m" # Inverted/Invertido la ele ||
S = "\033[8;30m" # Concealed/Encolhido       ||

