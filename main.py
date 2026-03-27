import os
import sys

# Adiciona src ao path para permitir importações absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.ui import main_banner, exibir_opcoes, credits_info, information, B, O
from src.config import websites
from src.api_client import data_information, busca_ip
from src.database import get_top_dns, get_dns_by_city, get_dns_by_country, get_all_dns_counts
from src.benchmark import testar_dns

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    main_banner()
    user_data = data_information()

    if not user_data:
        print("Não foi possível obter as informações do usuário. Saindo.")
        return

    country_code = user_data.get("country_code", "").upper()
    city = user_data.get("city", "").lower()

    while True:
        top_dns_count, city_dns_count, country_dns_count = get_all_dns_counts(city, country_code)
        exibir_opcoes(top_dns_count, city_dns_count, country_dns_count)
        opcao = input("Enter the number of the desired option: ")

        if opcao == "1":
            dns_list = get_top_dns()
            if dns_list:
                testar_dns(dns_list, websites)
            else:
                print("\nNo DNS server found in TOP DNS list.")
                input("Press Enter to continue...")
        elif opcao == "2":
            dns_list = get_dns_by_city(city)
            if dns_list:
                testar_dns(dns_list, websites)
            else:
                print("\nNo DNS servers found in your city.")
                input("Press Enter to continue...")
        elif opcao == "3":
            dns_list = get_dns_by_country(country_code)
            if dns_list:
                testar_dns(dns_list, websites)
            else:
                print("\nNo DNS servers found in your country.")
                input("Press Enter to continue...")

        elif opcao == "5":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                main_banner()
                busca_ip()
                nova = input(f"\n[{B}?{O}] Do you want to perform a new IP lookup? [Y/N]: ").lower()
                if nova not in ["y", "yes"]:
                    break
            os.system('cls' if os.name == 'nt' else 'clear')
            main_banner()

        elif opcao == "8":
            os.system('cls' if os.name == 'nt' else 'clear')
            information()
            input(f"Press Enter to continue... ") 
            os.system('cls' if os.name == 'nt' else 'clear')
            main_banner()

        elif opcao == "9":
            credits_info()
            input(f"Press Enter to continue... ") 
            os.system('cls' if os.name == 'nt' else 'clear')
            main_banner()

        elif opcao == "0":
            print(f"\nLeaving the program, see you soon!\n")
            break
        else:
            print("\nInvalid option. Please try again.")
            input("Press Enter to continue...")
        if opcao not in ["5", "0"]:
             os.system('cls' if os.name == 'nt' else 'clear')
             main_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by the user. Exiting the program safely")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
