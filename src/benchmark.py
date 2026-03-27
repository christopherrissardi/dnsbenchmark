import dns.resolver as resolver
import time
from src.ui import B, O, main_banner
from src.utils import salvar_resultados
import os

def validar_dns(dns_server, dominio_teste):
    try:
        resolver_instance = resolver.Resolver()
        resolver_instance.nameservers = [dns_server]
        inicio = time.time()
        resposta = resolver_instance.resolve(dominio_teste, 'A', raise_on_no_answer=False)
        fim = time.time()
        if resposta:
            tempo_resposta = (fim - inicio) * 1000
            print(f"{B}{dns_server}{O} responded to DNS validation on {tempo_resposta:.2f} ms.\n")
            return True
    except Exception:
        print(f"There was no response from the server {dns_server} for the domain {dominio_teste}.")
    return False

def medir_tempo_resposta(dns_server, dominio):
    try:
        resolver_instance = resolver.Resolver()
        resolver_instance.nameservers = [dns_server]
        inicio = time.time()
        resolver_instance.resolve(dominio, 'A', raise_on_no_answer=False)
        fim = time.time()
        tempo_resposta = (fim - inicio) * 1000
        return tempo_resposta 
    except Exception:
        return None 

def testar_dns(lista_dns, websites):
    if not lista_dns:
        print("No DNS servers available to test.")
        return

    print(f"\n{B}Testing {len(lista_dns)} DNS servers, please wait...{O}")
    resultados = []

    for dns in lista_dns:
        print(f"\nValidating DNS Server: {B}{dns['ip']}{O} | {dns.get('isp', 'N/A')} | {dns.get('city', 'Unknown')} - {dns.get('country_id', 'N/A')}{O}")
        print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if not validar_dns(dns['ip'], websites[0]):
            print(f"There was no response from DNS server {dns['ip']}. Ignoring...")
            continue

        print(f"Testing the DNS server: {B}{dns['ip']}{O}")
        
        tempos_resposta = []  
        for site in websites:
            tempo_resposta = medir_tempo_resposta(dns['ip'], site)
            if tempo_resposta is not None:
                tempos_resposta.append(tempo_resposta)
                print(f"Response time for {site}: {B}{tempo_resposta:.2f} ms.{O}")
            else:
                print(f"There was no response in time to the site {site}. Skipping test...")
        
        if tempos_resposta:
            media_tempo = sum(tempos_resposta) / len(tempos_resposta)
            provedor = dns.get('isp', 'Unknown Provider')
            resultados.append((dns['ip'], provedor, media_tempo))
            print(f"Average response time: {media_tempo:.2f} ms.")
        else:
            print("No valid response for this server. Ignoring...")

    resultados_ordenados = sorted(resultados, key=lambda x: x[2])
    salvar_resultados(resultados_ordenados)

    print(f"\n{B}Ranking of the best DNS servers for your home/location:{O}\n")
    for rank, (ip, provedor, tempo) in enumerate(resultados_ordenados, start=1):
        print(f"{rank}. {ip} - {B}{provedor}{O} - {tempo:.2f} ms")
    print(f"\n        +-------------------------------+\n        |     Benchmarks completed.     |\n        +-------------------------------+  \n          ")
    input(f"\nPress Enter to continue... ") 
    os.system('cls' if os.name == 'nt' else 'clear')
    main_banner()