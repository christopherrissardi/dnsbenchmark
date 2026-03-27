import socket
import os
from src.ui import B, O

def get_local_ip():
    """Obtém o endereço IP local da máquina."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # não precisa ser alcançável
        s.connect(('10.254.254.254', 1))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = 'Unavailable'
    finally:
        s.close()
    return ip_local

def get_username():
    """Obtém o nome de usuário logado no momento."""
    return os.getlogin()

def salvar_resultados(resultados_ordenados):
    """Salva os resultados do benchmark em results.txt."""
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("Ranking of the best DNS servers for your home/location:\n")
        for rank, (ip, provedor, tempo) in enumerate(resultados_ordenados, start=1):
            f.write(f"{rank}. {ip} - {provedor} - {tempo:.4f} ms\n")

    print(f"\nResults saved in the file '{B}results.txt{O}'.")
