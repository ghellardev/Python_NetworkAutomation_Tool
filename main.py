from napalm import get_network_driver
# from netmiko import ConnectHandler
# import subprocess
import json
from netmiko import ConnectionException
from netmiko import NetmikoBaseException
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException


def filtrare_lista_ip(lista1):
    lista_buna = []
    if lista1:
        for i in lista1:
            octeti = i.split(".")
            for j in octeti:
                if len(octeti) == 4:
                    if j.isdigit():
                        if int(j) not in range(0, 256):
                            break
                    else:
                        break
                else:
                    break
            else:
                lista_buna.append(".".join(octeti))
        print(lista_buna)
        if lista_buna:
            return lista_buna
        else:
            return "The list is empty"
    else:
        return "The list is empty"


def conectiv1(lista_echipamente):
    try:
        for ip_eq in lista_echipamente:
            driver = get_network_driver("ios")
            echipament = driver(ip_eq, "admin", "savnet", optional_args={'global_delay_factor': 2})
            echipament.open()
            driver = get_network_driver("ios")
            echipament = driver(ip_eq, "admin", "savnet")
            d = echipament.get_facts()
            res = json.dumps(echipament.get_config(retrieve='running'), indent=4)
            stres = res.split("\n")
            hostname = d['hostname']

            with open(f"{hostname}.txt", 'w') as ff:
                print(f"Configuratia este momentan in curs de preloare de la {hostname} cu adresa IP {ip_eq}")
                ff.writelines(stres)
    except NetmikoTimeoutException:
        print(f"Equipmentul cu ip timed out")
    except NetmikoAuthenticationException:
        print(f"Esuare la autentificare")
    except ConnectionException:
        print(f"Conexiune esuata")
    except NetmikoBaseException:
        print(f"eroare de baza")


def conectiv2(lista_echipamente):
    try:
        for ip_eq in lista_echipamente:
            driver = get_network_driver("ios")
            echipament = driver(ip_eq, "admin", "savnet", optional_args={'global_delay_factor': 2})
            echipament.open()
            driver = get_network_driver("ios")
            echipament = driver(ip_eq, "admin", "savnet")
            echipament.get_config(retrieve='running')
            d = echipament.get_facts()
            hostname = d['hostname']
            print(f'This is a config to be added on {ip_eq}:\n')

            with open(f'{hostname}.txt', 'r'):

                echipament.load_merge_candidate(filename=f"{hostname}.txt")

                print(echipament.compare_config())

                confirm_config = input('Do you want to deploy the above config? Press Y to deploy \n '
                                       'Press anything else to cancel:')

                if confirm_config == 'Y':
                    echipament.commit_config()
                    echipament.close()
                elif confirm_config == 'y':
                    echipament.commit_config()
                    echipament.close()
                else:
                    echipament.close()
    except NetmikoTimeoutException:
        print(f"Equipmentul cu ip timed out")
    except NetmikoAuthenticationException:
        print(f"Esuare la autentificare")
    except ConnectionException:
        print(f"Conexiune esuata")
    except NetmikoBaseException:
        print(f"eroare de baza")


def conectiv9(lista_echipamente):
    try:
        for ip_eq in lista_echipamente:
            driver = get_network_driver("ios")
            echipament = driver(ip_eq, "admin", "savnet", optional_args={'global_delay_factor': 2})
            echipament.open()
            for ip in lista_echipamente:
                print(f"Currently sending ping from {ip_eq}")
                if ip != ip_eq:
                    output = echipament.ping(ip)
                    print(json.dumps(output, indent=4))
                echipament.close()
    except NetmikoTimeoutException:
        print(f"Equipmentul cu ip timed out")
    except NetmikoAuthenticationException:
        print(f"Esuare la autentificare")
    except ConnectionException:
        print(f"Conexiune esuata")
    except NetmikoBaseException:
        print(f"eroare de baza")


def main():
    with open('lista.txt') as f:
        lista_echipamente = f.read().splitlines()
    lista_valida = filtrare_lista_ip(lista_echipamente)

    while True:
        if lista_valida == "The list is empty":
            print("Eroare, lista este goala")
            break
        meniu = input('''Apăsați:
        1 pentru extragerea configurarii
        2 pentru a aplica o configurare
        9 pentru verificarea conectivității IP specific din rețea - toate IP-urile din rețea
        q pentru ieșire\n''')
        if meniu == 'q':
            break
        elif meniu == '9':
            conectiv9(lista_valida)
        elif meniu == '1':
            conectiv1(lista_valida)
        elif meniu == '2':
            conectiv2(lista_valida)
        else:
            print("Opțiune invalidă!")


main()
