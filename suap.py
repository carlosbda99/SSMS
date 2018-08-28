#!/usr/bin/python3

# Importing libraries
import requests
from getpass import getpass
from os import system
from time import sleep

# Declaring variables
login = ''
password = ''
year = ''
period = ''

# Starting program
def authentication():
    print("Sistema de Suporte de Material do SUAP")
    login = input("Digite o seu login: ")
    password = getpass(prompt="Digite a sua senha: ")
    queue = requests.post("https://suap.ifrn.edu.br/api/v2/autenticacao/token/?format=json",json={'username': login, 'password': password})
    token = queue.json()
    token = token['token']
    if queue.status_code == 200:
        print("Autenticado\n!\n!")
        main(token)
    else:
        print("Erro de autenticação!")
        sleep(2)
        system("clear")
        authentication()

def main(token):
    print("Bem vindo ao Sistema de Suporte de Material do SUAP")
    year = input("Digite o ano que deseja realizar o download de materiais: ")
    period = input("Selecione o período desejado: ")
    print('Realizando download, aguarde...')
    if not (period == '1' or period == '2'):
        print("Entrada incorreta, tente novamente (1 ou 2)")
        sleep(2)
        system("clear")
        main()
    bulletin = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/%s/%s/'%(year,period), headers={'Authorization' : 'JWT ' + token})
    if bulletin.status_code == 200:
        grade = bulletin.json()
    else:
        print('Erro, tente novamente')
        grade = bulletin.json()
        sleep(2)
        system('clear')
        main()
    try:
        for x in grade:
            if x!='detail':
                codAd=str(x['codigo_diario'])
                queue = requests.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/%s/'%codAd, headers={'Authorization' : 'JWT ' + token})
                if queue.status_code == 200:
                    classV = queue.json()
                    directory = x['disciplina'].replace('/','-').split(' ')
                    directory = '_'.join(directory)
                    system ('mkdir -p \"%s-%s/%s\"'%(year,period,directory))
                    for x in classV['materiais_de_aula']:
                        if x['url'][0]=='/':
                            link = 'https://suap.ifrn.edu.br' +(x['url'])
                            system ('wget -nv -N -P \"%s-%s/%s\" \"%s\"'%(year,period,directory,link))
                        else:
                            link = x['url']
                            system ('echo \"%s\" > \"%s-%s/%s/Link_de_naterial\"'%(link,year,period,directory))
                elif queue.status_code == 404:
                    print('Erro, tente novamente')
        print('Download realizado')
    except:
        print('Houve algum erro ao realizar o download, desculpe!')

#main()
authentication()
