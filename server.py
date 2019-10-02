from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

class Servidor(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.traduzNumero(self.path[1:])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())
        return

    def traduzNumero(self, numero):
        
        extenso1_19 = {1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez',
        11: 'onze', 12: 'doze', 13: 'treze', 14: 'quatorze', 15: 'quinze', 16: 'dezesseis', 17: 'dezessete', 18: 'dezoito', 19: 'dezenove'}
        extenso_dezenas = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
        extenso_milhares = " mil"

        #retira os zeros a esquerda do numero
        while (numero[0] == '0'):
            numero = numero[1:]

        numero_entrada = int(numero)
        #inicializa a string onde eh armazenada a traducao do numero.
        numero_traduzido = ""

        '''
            testa se o numero eh negativo, se sim, adiciona a palavra "menos" a traducao e segue o processo de traducao
            pulando o caracter do sinal negativo
        '''
        if numero_entrada < 0:
            numero_traduzido = "menos "
            numero_entrada = str(numero_entrada)
            numero_entrada = numero_entrada[1:]
        
        numero_entrada = str(numero_entrada)
        #testa o tamanho do numero, se for igual a 5 a traducao fica com 10-99 mil em extenso
        if len(numero_entrada) == 5:
            #digito1 e 2 correspondem as duas primeiras casas do numero, as dezenas dos milhares
            digito1 = numero_entrada[0]
            digito2 = numero_entrada[1]
            '''
                se as duas primeiras casas do digito forem menor que 19, entra em um caso especial, pois esses
                numeros sao escritos de maneira diferente aos demais
            '''
            if int(digito1 + digito2) <= 19:
                dezena = int(digito1 + digito2)
                numero_traduzido = numero_traduzido + str(extenso1_19[dezena]) + extenso_milhares
                return self.traduzNumeroCentenas(str(numero_entrada[2:]), numero_traduzido)
            else:
                #caso padrao das dezenas
                dezena = int(digito1) - 2
                if digito2 == '0':
                    #se o segundo digito das dezenas for 0, a dezena eh redonda
                    numero_traduzido = numero_traduzido + extenso_dezenas[dezena] + extenso_milhares + " e "
                    return self.traduzNumeroCentenas(str(numero_entrada[2:]), numero_traduzido)
                else:
                    #senao o nome da dezena tera que ser somado com o nome do numero quebrado da dezena
                    #Exemplo: 84 = oitenta + quatro
                    numero_traduzido = numero_traduzido + extenso_dezenas[dezena] + " e " + extenso1_19[int(digito2)] + extenso_milhares + " "
                    return self.traduzNumeroCentenas(str(numero_entrada[1:]), numero_traduzido)
        
        #se o numero possuir quatro digitos, a traducao fica com 1-9 mil em extenso
        if len(numero_entrada) == 4:
            numero_traduzido = numero_traduzido + extenso1_19[int(numero_entrada[0])] + extenso_milhares + " "
            return self.traduzNumeroCentenas(str(numero_entrada[1:]), numero_traduzido)

        #se o numero possuir 3 digitos, se e passado a funcao utilizada para traduzir a parte das centenas do numero
        if len(numero_entrada) == 3:
            return self.traduzNumeroCentenas(numero_entrada, numero_traduzido)
        
        #se o numero possuir 2 ou menos numeros, se e passado a funcao utilizada na traducao das dezenas do numero
        if len(numero_entrada) <= 2:
            return self.traduzNumeroDezenas(numero_entrada, numero_traduzido)

    def traduzNumeroCentenas (self, restante, numero_traduzido):

        extenso_centenas = ['cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
        
        #se for passado um numero terminado em 100 o programa ira retornar "cento", teria que tratar o final 100 de maneira especial
        if (restante == '100'):
            numero_traduzido = numero_traduzido + "cem"
            print("traduzido", numero_traduzido)
            return numero_traduzido

        if (restante[0] == '0'):
            return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)

        if (restante[1] == '0'):
            if (restante[2] == '0'):
                print("traduzido", numero_traduzido)
                return numero_traduzido
            else:
                numero_traduzido = numero_traduzido + extenso_centenas[int(restante[0]) - 1]
                print("traduzido", numero_traduzido)
                return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)
        else:
            numero_traduzido = numero_traduzido + extenso_centenas[int(restante[0]) - 1]
            print("entrando aqui", numero_traduzido)
            return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)
            
        '''
        else:
            dezena = int(restante[1]) - 2
            if (restante[2] == '0'):
                numero_traduzido = numero_traduzido + extenso_centenas[int(restante[0])] + " e " + extenso_dezenas[dezena]
                print("traduzido", numero_traduzido)
                return numero_traduzido
            else:
                unidade = int(restante[2]) - 1
                numero_traduzido = numero_traduzido + extenso_centenas[int(restante[0])] + " e " + extenso_dezenas[dezena] + " e " + extenso1_19[unidade]
                print("traduzido", numero_traduzido)
                return numero_traduzido  
        '''

    def traduzNumeroDezenas(self, restante, numero_traduzido):

        extenso1_19 = {1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez',
        11: 'onze', 12: 'doze', 13: 'treze', 14: 'quatorze', 15: 'quinze', 16: 'dezesseis', 17: 'dezessete', 18: 'dezoito', 19: 'dezenove'}
        extenso_dezenas = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']

        if ((restante[0] == '0') and (restante[1] == '0')):
            print("zxczxczxc", restante[1])
            print("traduzido", numero_traduzido)
            return numero_traduzido

        print("asdasd", restante[1])
        if int(restante[0] + restante[1]) <= 19:
            print("asdasd", restante[1])
            dezena = int(restante[0] + restante[1])
            numero_traduzido = numero_traduzido + " e " + extenso1_19[dezena]
            print("final", numero_traduzido)
            return numero_traduzido
        else:
            print("asdasd", restante[1])
            if (restante[1] == '0'):
                print("elefante")
                numero_traduzido = numero_traduzido + " e " + extenso_dezenas[int(restante[0]) - 2]
                print("resto", numero_traduzido)
                return numero_traduzido
            else:
                numero_traduzido = numero_traduzido + " e " + extenso_dezenas[int(restante[0]) - 2] + " e " + extenso1_19[int(restante[1])]
                print("resto", numero_traduzido)
                return numero_traduzido
        '''
        if (restante[1] == '0'):
            
            numero_traduzido = numero_traduzido + 
        '''

porta = 3000
servidor = HTTPServer(('localhost', porta), Servidor)
print('Iniciando o servidor http://localhost:', porta)
servidor.serve_forever()