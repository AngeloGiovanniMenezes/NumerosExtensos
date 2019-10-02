from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

class Servidor(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        traducao = Tradutor(self.path[1:])
        traduzido = traducao.getTraduzido()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'extenso': traduzido,
        }).encode())
        return

class Tradutor():

    extenso1_19 = {1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez',
    11: 'onze', 12: 'doze', 13: 'treze', 14: 'quatorze', 15: 'quinze', 16: 'dezesseis', 17: 'dezessete', 18: 'dezoito', 19: 'dezenove'}
    extenso_dezenas = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
    extenso_centenas = ['cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
    extenso_milhares = " mil"

    def __init__(self, numero):
        
        #inicializa a string onde eh armazenada a traducao do numero.
        self.numero_traduzido = ""

        self.numero_entrada = self.removeZerosEsquerda(numero)
        if (self.checaIntervalo() == True):
            self.testaNegativo(self.numero_entrada, self.numero_traduzido) 
            self.numero_entrada = str(self.numero_entrada)
            self.numero_traduzido = self.traduzNumero(self.numero_entrada, self.numero_traduzido)
        else:
            self.numero_traduzido = "Numero fora do intervalo"

    def getTraduzido(self):

        print(self.numero_traduzido)
        return self.numero_traduzido

    def checaIntervalo(self):

        if ((self.numero_entrada < -99999) or (self.numero_entrada > 99999)):
            return False
        else:
            return True

    '''
        remove todos os zeros a esquerda do numero
    '''
    def removeZerosEsquerda(self, numero):

        while (numero[0] == '0'):
            numero = numero[1:]
        
        numero = int(numero)
        return numero

    '''
        testa se o numero eh negativo, se sim, adiciona a palavra "menos" a traducao e segue o processo de traducao
        pulando o caracter do sinal negativo
    '''
    def testaNegativo(self, numero_entrada, numero_traduzido):

        if (self.numero_entrada < 0):
            self.numero_traduzido = "menos "
            self.numero_entrada = str(self.numero_entrada)
            self.numero_entrada = self.numero_entrada[1:]

    def traduzNumero(self, numero, numero_traduzido):

        #testa o tamanho do numero, se for igual a 5 a traducao fica com 10-99 mil em extenso
        if (len(numero) == 5):
            redondo = int(numero[1:])
            if (redondo == 0):
                if(numero[0] == '1'):   #caso especifico para o dez mil
                    numero_traduzido = self.extenso1_19[int(numero[0] + numero[1])] + self.extenso_milhares
                    return numero_traduzido
                else:   #caso para os demais numeros com o padrao de dezenas de milhar redondos. Exemplo(30000)
                    numero_traduzido = self.extenso_dezenas[int(numero[0]) - 1] + self.extenso_milhares
                    return numero_traduzido
            else:   #caso para os numeros com dezenas de milhares e numeros quebrados. Exemplo(41987)
                numero_traduzido = self.traduzNumeroDezenas(str(numero[:2]), numero_traduzido)
                numero_traduzido = numero_traduzido + self.extenso_milhares + " e "
                return self.traduzNumeroCentenas(str(numero[2:]), numero_traduzido)

        #se o numero possuir quatro digitos, a traducao fica com 1-9 mil em extenso
        if (len(numero) == 4):
            
            redondo = int(numero[1:])
            if (redondo == 0):  #caso para os numeros com 4 casas redondos. Exemplo(1000)
                numero_traduzido = self.extenso1_19[int(numero[0])] + self.extenso_milhares
                return numero_traduzido
            else:   #caso para os numeros com 4 casas quebrados. Exemplo(5420)
                numero_traduzido = numero_traduzido + self.extenso1_19[int(numero[0])] + self.extenso_milhares + " e "
                return self.traduzNumeroCentenas(str(numero[1:]), numero_traduzido)

        #se o numero possuir 3 digitos, se e passado a funcao utilizada para traduzir a parte das centenas do numero
        if (len(numero) == 3):
            return self.traduzNumeroCentenas(numero, numero_traduzido)
        
        #se o numero possuir 2 ou menos numeros, se e passado a funcao utilizada na traducao das dezenas do numero
        if (len(numero) <= 2):
            return self.traduzNumeroDezenas(numero, numero_traduzido)

    def traduzNumeroCentenas (self, restante, numero_traduzido):

        #se for passado um numero terminado em 100 o programa ira retornar "cento", teria que tratar o final 100 de maneira especial
        if (restante == '100'):
            
            numero_traduzido = numero_traduzido + "cem"
            return numero_traduzido

        if (restante[0] == '0'):    #se o primeiro numero da centena, entao temos apenas as dezenas, sendo assim a funcao para as centenas eh chamada.
            return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)

        if (restante[1] == '0'):
            if (restante[2] == '0'):    #caso para as demais dezenas redondas. Exemplo(300)
                numero_traduzido = numero_traduzido + self.extenso_centenas[int(restante[0]) - 1]
                return numero_traduzido
            else:   #caso para as centenas sem dezenas. Exemplo(405), chama-se a funcao de dezenas pois esta esta encarregada de numeros com duas casas
                numero_traduzido = numero_traduzido + self.extenso_centenas[int(restante[0]) - 1] + " e "
                return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)
        else:   #caso para as centenas com numeros quebrados. Exemplo(777)
            numero_traduzido = numero_traduzido + self.extenso_centenas[int(restante[0]) - 1] + " e "
            return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)

    def traduzNumeroDezenas(self, restante, numero_traduzido):

        if (len(restante) == 1):    #caso para numeros de 1-9
            numero_traduzido = self.extenso1_19[int(restante)]
            return numero_traduzido

        if ((restante[0] == '0') and (restante[1] == '0')): #caso para dezena 00
            return numero_traduzido

        if (int(restante[0] + restante[1]) <= 19):  #caso para as dezenas especiais 1-19
            dezena = int(restante[0] + restante[1])
            if (numero_traduzido == ''):    #caso para numeros de duas casas
                numero_traduzido =  self.extenso1_19[dezena]
                return numero_traduzido
            else:   #caso para numeros com mais de duas casas
                numero_traduzido = numero_traduzido  + self.extenso1_19[dezena]
                return numero_traduzido
        else: 
            if (restante[1] == '0'):    #caso para numeros com dezenas redondas. Exemplo(50)
                numero_traduzido = numero_traduzido  + self.extenso_dezenas[int(restante[0]) - 2]
                return numero_traduzido
            else:   #caso para numeros com dezenas quebradas. Exemplo(38)
                numero_traduzido = numero_traduzido + self.extenso_dezenas[int(restante[0]) - 2] + " e " + self.extenso1_19[int(restante[1])]
                return numero_traduzido

porta = 3000
servidor = HTTPServer(('localhost', porta), Servidor)
print('Iniciando o servidor http://localhost:', porta)
servidor.serve_forever()