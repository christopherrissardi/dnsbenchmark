
import os
import json
import dns.resolver as resolver
import time
import requests
import whois

from utils import main_banner, data_information, information
from domains import websites
from credits import credits_info

B = "\033[0;31m"  # Vermelho
O = "\033[1;37m"  # Branco
H = "\033[1;30m"  # Preto 2

os.system('cls' if os.name == 'nt' else 'clear')

def carregar_json(caminho_arquivo):

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file {caminho_arquivo}: {e}")
        return None

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
        print(f"\nValidating DNS Server: {B}{dns['ip']}{O} | {dns['isp']} | {dns.get('city', 'Unknown')} - {dns['country_id']}{O}")
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
    print(f"""
        +-------------------------------+  
        |     Benchmarks completed.     |
        +-------------------------------+  
          """)
    print(f"Results saved in the file '{B}results.txt{O}'.\n")
    input(f"\nPress Enter to continue... ") 
    os.system('cls' if os.name == 'nt' else 'clear')

    main_banner()

def salvar_resultados(resultados_ordenados):

    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("Ranking of the best DNS servers for your home/location:\n")
        for rank, (ip, provedor, tempo) in enumerate(resultados_ordenados, start=1):
            f.write(f"{rank}. {ip} - {provedor} - {tempo:.4f} ms\n")

    print("Results saved in the file 'results.txt'.\n")

def exibir_opcoes(top_dns_count, city_dns_count, country_dns_count):

    print("\nChoose one of the test options:\n")
    print(f"[{B}1{O}] DNS benchmark test with most popular servers [TOP-DNS]. ({B}{top_dns_count}{O} servers).")
    print(f"[{B}2{O}] DNS benchmark test with servers in your city. ({B}{city_dns_count}{O} servers available in your city).")
    print(f"[{B}3{O}] DNS benchmark test with servers in your country. ({B}{country_dns_count}{O} servers available in your country).")
    print(f"[{B}4{O}] DNS benchmark test with global valid servers. (Coming soon)")
    print(f"[{B}5{O}] DNS or IP Geolocation Lookup - Search for information about any IP address.")
    print(f"")
    print(f"[{B}9{O}] Credits.")
    print(f"[{B}0{O}] Exit.\n")

def main():

    os.system('cls' if os.name == 'nt' else 'clear')

    main_banner()
    user_data = data_information()

    if not user_data:
        return

    country_code = user_data.get("country_code").lower()
    city = user_data.get("city", "").lower()

    arquivo_pais = os.path.join("data", f"{country_code}.json")
    dados_pais = carregar_json(arquivo_pais)
    if not dados_pais:
        return

    top_dns_path = os.path.join("data", "top_dns.json")
    top_dns = carregar_json(top_dns_path)
    top_dns_count = len(top_dns) if top_dns else 0

    dns_cidade = [dns for dns in dados_pais if dns.get("city", "").lower() == city]
    city_dns_count = len(dns_cidade)
    country_dns_count = len(dados_pais)

    while True:
        exibir_opcoes(top_dns_count, city_dns_count, country_dns_count)

        opcao = input("Enter the number of the desired option: ")

        if opcao == "1":
            if top_dns:
                testar_dns(top_dns, websites)
            else:
                print("\nNo DNS server found in TOP DNS list.")
                input("Press Enter to continue...")
        elif opcao == "2":
            if dns_cidade:
                testar_dns(dns_cidade, websites)
            else:
                print("No DNS servers found in your city.")
                input("Press Enter to continue...")
        elif opcao == "3":
            testar_dns(dados_pais, websites)

        elif opcao == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            main_banner()
            busca_ip()       
    
        elif opcao == "8":

            os.system('cls' if os.name == 'nt' else 'clear')
            information()
            input(f"Press Enter to continue... ") 
            print("\n")
            main()  

        elif opcao == "9":
            os.system('cls' if os.name == 'nt' else 'clear')
            credits_info()
            input(f"Press Enter to continue... ") 
            print("\n")
            main()       

        elif opcao == "0":
            print(f"Leaving the program, see you soon!\n")
            os._exit(0)
            break
        else:
            print("\nInvalid option. Please try again.")
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            main()


def busca_ip():

    ip = input(f"\n[{B}*{O}] Enter the IP address to be queried: ")
    url = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query')

    json = url.json()

    if url.status_code == 200:

        if json.get('status') == 'fail':
            print(f"[{B}!{O}] IP address {ip} not found.")
        else:
            print("")
            print(f"[{B}+{O}] Status:", json.get('status') or 'Unknown')
            print(f"[{B}+{O}] IP:", json.get('query') or 'Unknown')
            print(f"[{B}+{O}] City:", json.get('city') or 'Unknown', f"({json.get('region')})")
            print(f"[{B}+{O}] Region:", json.get('regionName') or 'Unknown')
            print(f"[{B}+{O}] Country:", json.get('country') or 'Unknown')
            print(f"[{B}+{O}] Continent:", json.get('continent') or 'Unknown', f"({json.get('region')})")
            print(f"[{B}+{O}] Latitude:", json.get('lat') or 'Unknown')
            print(f"[{B}+{O}] Longitude:", json.get('lon') or 'Unknown')
            print(f"[{B}+{O}] ISP:", json.get('isp') or 'Unknown')
            print(f"[{B}+{O}] Org:", json.get('org') or 'Unknown')
            print(f"[{B}+{O}] AS:", json.get('as') or 'Unknown')
            print(f"[{B}+{O}] ASNAME:", json.get('asname') or 'Unknown')
            print(f"[{B}+{O}] IP Proxy:", json.get('proxy') or 'Unknown')
            print(f"[{B}+{O}] Reverse IP:", json.get('reverse') or 'Unknown')
            print(f"[{B}+{O}] ZIP Code Of State:", json.get('zip') or 'Unknown')
            print(f"[{B}+{O}] IP Hosting:", json.get('hosting') or 'Unknown')
            print(f"[{B}+{O}] Currency:", json.get('currency') or 'Unknown')
            print(f"[{B}+{O}] Time Zone:", json.get('timezone') or 'Unknown')
            print("")

            print(f"[{B}!{O}] Performing WHOIS lookup...")
            try:
                whois_data = whois.whois(ip)

                print("\n-> WHOIS Data Lookup:\n")
                for key, value in whois_data.items():
                    print(f"[{B}+{O}] {key}: {value}")
            except Exception as e:
                print(f"[{B}!{O}] Error fetching WHOIS data: {e}")
                whois_data = None

            salvar_arquivo = input(f"\n[{B}?{O}] Do you want to save the results to a file? [Y/N]: ").lower()

            if salvar_arquivo in ["y", "yes"]:
                ip_caminho = f"{ip}.txt"
                caminho_arquivo = os.path.join(os.getcwd(), ip_caminho)

                with open(caminho_arquivo, 'w') as arquivo:

                    arquivo.write(f"IP Search Results - {ip}\n\n")
                    arquivo.write(f"[+] Status: {json.get('status') or 'Unknown'}\n")
                    arquivo.write(f"[+] IP: {json.get('query') or 'Unknown'}\n")
                    arquivo.write(f"[+] City: {json.get('city') or 'Unknown'} ({json.get('region')})\n")
                    arquivo.write(f"[+] Region: {json.get('regionName') or 'Unknown'}\n")
                    arquivo.write(f"[+] Country: {json.get('country') or 'Unknown'}\n")
                    arquivo.write(f"[+] Continent: {json.get('continent') or 'Unknown'} ({json.get('region')})\n")
                    arquivo.write(f"[+] Latitude: {json.get('lat') or 'Unknown'}\n")
                    arquivo.write(f"[+] Longitude: {json.get('lon') or 'Unknown'}\n")
                    arquivo.write(f"[+] ISP: {json.get('isp') or 'Unknown'}\n")
                    arquivo.write(f"[+] Org: {json.get('org') or 'Unknown'}\n")
                    arquivo.write(f"[+] AS: {json.get('as') or 'Unknown'}\n")
                    arquivo.write(f"[+] ASNAME: {json.get('asname') or 'Unknown'}\n")
                    arquivo.write(f"[+] IP Proxy: {json.get('proxy') or 'Unknown'}\n")
                    arquivo.write(f"[+] Reverse IP: {json.get('reverse') or 'Unknown'}\n")
                    arquivo.write(f"[+] ZIP Code Of State: {json.get('zip') or 'Unknown'}\n")
                    arquivo.write(f"[+] IP Hosting: {json.get('hosting') or 'Unknown'}\n")
                    arquivo.write(f"[+] Currency: {json.get('currency') or 'Unknown'}\n")
                    arquivo.write(f"[+] Time Zone: {json.get('timezone') or 'Unknown'}\n\n")
                    
                    arquivo.write(f"WHOIS Data:\n\n")
                    if whois_data:
                        for key, value in whois_data.items():
                            arquivo.write(f"{key}: {value}\n")
                    else:
                        arquivo.write("WHOIS data could not be retrieved.\n")

                print(f"")
                print(f"+-------------------------------------------------------------------------+")
                print(f"    The results were successfully saved to the file {B}{ip_caminho}{O}"     )
                print(f"+-------------------------------------------------------------------------+")
                print(f"")
        
        nova = input(f"[{B}?{O}] Do you want to perform a new IP lookup? [Y/N]: "
                ).lower()
        os.system('cls' if os.name == 'nt' else 'clear')

        if nova == "y" or nova == "yes":
            main_banner()
            busca_ip()
        else:
            main()

    else:
        print(f"[{B}!{O}] Error with the IP request.")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by the user. Exiting the program safely")
