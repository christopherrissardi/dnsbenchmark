import os

# --- Cores ---
B = "\033[0;31m"  # Vermelho
O = "\033[1;37m"  # Branco
H = "\033[1;30m"  # Preto 2

def main_banner():
    print(rf"""{B}                                                                                                                                                  
{O}       ┏━╸╻  ┏━┓┏┓ ┏━┓╻  {B} ╺┳┓┏┓╻┏━┓
{O}       ┃╺┓┃  ┃ ┃┣┻┓┣━┫┃  {B}  ┃┃┃┗┫┗━┓
{O}       ┗━┛┗━╸┗━┛┗━┛╹ ╹┗━╸{B} ╺┻┛╹ ╹┗━┛
{O}          {H}┏┓ ┏━╸┏┓╻┏━╸╻ ╻┏┳┓┏━┓┏━┓╻┏     Powered By {B}Christopher Rissardi{O}
{O}          {H}┣┻┓┣╸ ┃┗┫┃  ┣━┫┃┃┃┣━┫┣┳┛┣┻┓   
{O}          {H}┗━┛┗━╸╹ ╹┗━╸╹ ╹╹ ╹╹ ╹╹┗╸╹ ╹                                                           
{O}                          
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

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

def credits_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    main_banner()
    print(f"""
    {B}My GitHub:{O} https://github.com/christopherrissardi     
        
    Thank you very much for using the tool! I hope it can contribute in some way to your goals
    of finding the best DNS server for your home/work/company or whatever! :)
    """)
