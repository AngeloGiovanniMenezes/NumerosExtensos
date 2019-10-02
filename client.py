import sys
import requests

path = "http://localhost:3000/"

if len(sys.argv) == 1:
    numero = input("Informe um valor inteiro para ser traduzido entre [-99999, 99999]: ")
else:
    numero = sys.argv[1]

def checa_intervalo(numero):
    if numero < -99999 or numero > 99999:
        return False
    else:
        return True


while True:
    try:
        testa_int = int(numero)
        if checa_intervalo(int(numero)) is True:
            path = path + str(numero)
            JSON_traduzido = requests.get(path)
            print(JSON_traduzido.content)
            break
        else:
            numero = input("Informe um valor inteiro para ser traduzido entre [-99999, 99999]: ")
    except ValueError:
        numero = input("Por favor, informe um valor inteiro a ser traduzido: ")
