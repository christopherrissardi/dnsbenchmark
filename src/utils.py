import socket
import os
import datetime
from src.ui import B, O

def get_local_ip():
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

def get_username(): # PEGA O NOME DE USUÁRIO LOGADO
    return os.getlogin()

def salvar_resultados(resultados_ordenados):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_resultados = "results"
    nome_arquivo = f"results_{timestamp}.txt"
    caminho_completo = os.path.join(pasta_resultados, nome_arquivo)
    os.makedirs(pasta_resultados, exist_ok=True)
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write("Ranking of the best DNS servers for your home/location:\n")
        for rank, (ip, provedor, tempo) in enumerate(resultados_ordenados, start=1):
            f.write(f"{rank}. {ip} - {provedor} - {tempo:.4f} ms\n")

    print(f"\nResults saved in the file '{B}results.txt{O}'.")
