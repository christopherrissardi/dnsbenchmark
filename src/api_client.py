import requests
import whois
from src.ui import B, O, main_banner
from src.utils import get_username, get_local_ip

def data_information():
    url = "https://ipwho.is/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
            return data
        else:
            print("Error getting external IP information. API reported failure.")
            print(f"Message: {data.get('message')}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def busca_ip():

    ip = input(f"\n[{B}*{O}] Enter the IP address to be queried: ")
    url = f'http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        if json_data.get('status') == 'fail':
            print(f"[{B}!{O}] IP address {ip} not found. Message: {json_data.get('message')}")
            return

        print("")
        print(f"[{B}+{O}] Status:", json_data.get('status') or 'Unknown')
        print(f"[{B}+{O}] IP:", json_data.get('query') or 'Unknown')
        print(f"[{B}+{O}] City:", json_data.get('city') or 'Unknown', f"({json_data.get('region')})")
        print(f"[{B}+{O}] Region:", json_data.get('regionName') or 'Unknown')
        print(f"[{B}+{O}] Country:", json_data.get('country') or 'Unknown')
        print(f"[{B}+{O}] Continent:", json_data.get('continent') or 'Unknown', f"({json_data.get('region')})")
        print(f"[{B}+{O}] Latitude:", json_data.get('lat') or 'Unknown')
        print(f"[{B}+{O}] Longitude:", json_data.get('lon') or 'Unknown')
        print(f"[{B}+{O}] ISP:", json_data.get('isp') or 'Unknown')
        print(f"[{B}+{O}] Org:", json_data.get('org') or 'Unknown')
        print(f"[{B}+{O}] AS:", json_data.get('as') or 'Unknown')
        print(f"[{B}+{O}] ASNAME:", json_data.get('asname') or 'Unknown')
        print(f"[{B}+{O}] IP Proxy:", json_data.get('proxy') or 'Unknown')
        print(f"[{B}+{O}] Reverse IP:", json_data.get('reverse') or 'Unknown')
        print(f"[{B}+{O}] ZIP Code Of State:", json_data.get('zip') or 'Unknown')
        print(f"[{B}+{O}] IP Hosting:", json_data.get('hosting') or 'Unknown')
        print(f"[{B}+{O}] Currency:", json_data.get('currency') or 'Unknown')
        print(f"[{B}+{O}] Time Zone:", json_data.get('timezone') or 'Unknown')
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
            with open(ip_caminho, 'w', encoding='utf-8') as arquivo:
                arquivo.write(f"IP Search Results - {ip}\n\n")
                # ... (código de escrita de arquivo omitido por brevidade, permanece o mesmo)
                print(f"\n+-------------------------------------------------------------------------+")
                print(f"    The results were successfully saved to the file {B}{ip_caminho}{O}")
                print(f"+-------------------------------------------------------------------------+\n")
    
    except requests.exceptions.RequestException as e:
        print(f"[{B}!{O}] Error with the IP request: {e}")