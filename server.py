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

        numero_entrada = int(numero)
        if numero_entrada < 0:
            
            numero_traduzido = "menos"
            print("entrou", numero_traduzido)
            numero_entrada = str(numero_entrada)
            numero_entrada = numero_entrada[1:]
        
        numero_entrada = str(numero_entrada)
        if len(numero_entrada) == 5:
            digito1 = numero_entrada[0]
            digito2 = numero_entrada[1]
            if int(digito1 + digito2) <= 19:
                dezena = int(digito1 + digito2)
                numero_traduzido = str(extenso1_19[dezena]) + extenso_milhares
                return self.traduzNumeroCentenas(str(numero_entrada[2:]), numero_traduzido)
            else:
                dezena = int(digito1) - 2
                if digito2 == '0':
                    numero_traduzido = extenso_dezenas[dezena - 1] + extenso_milhares
                    return self.traduzNumeroCentenas(str(numero_entrada[2:]), numero_traduzido)
                else:
                    numero_traduzido = extenso_dezenas[dezena] + " e " + extenso1_19[int(digito2)] + extenso_milhares
                    return self.traduzNumeroCentenas(str(numero_entrada[2:]), numero_traduzido)
        if len(numero_entrada) == 4:
            numero_traduzido = extenso1_19[int(numero_entrada[0])] + extenso_milhares
            return self.traduzNumeroCentenas(str(numero_entrada[1:]), numero_traduzido)

    def traduzNumeroCentenas (self, restante, numero_traduzido):

        extenso1_19 = {1: 'um', 2: 'dois', 3: 'três', 4: 'quatro', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove', 10: 'dez',
        11: 'onze', 12: 'doze', 13: 'treze', 14: 'quatorze', 15: 'quinze', 16: 'dezesseis', 17: 'dezessete', 18: 'dezoito', 19: 'dezenove'}
        extenso_dezenas = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
        extenso_centenas = ['cem', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']

        if (restante[0] == '0'):
            return self.traduzNumeroDezenas(str(restante[1:]), numero_traduzido)

        if (restante[1] == '0'):
            if (restante[2] == '0'):
                print("traduzido", numero_traduzido)
                return numero_traduzido
            else:
                numero_traduzido = numero_traduzido + extenso_centenas[int(restante[0])]
                print("traduzido", numero_traduzido)
                return numero_traduzido
        else:
            numero_traduzido = numero_traduzido + extenso_centenas[int(restante[0])] + " e " + extenso1_19[int(restante[2])]
            print("traduzido", numero_traduzido)
            return numero_traduzido
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

        if(restante[0] and restante[1]) == '0':
            print("traduzido", numero_traduzido)
            return numero_traduzido

        if int(restante[0] + restante[1]) <= 19:
                dezena = int(restante[0] + restante[1])
                numero_traduzido = numero_traduzido + " e " + str(extenso1_19[dezena])
                print("traduzido", numero_traduzido)
                return numero_traduzido
        '''
        if (restante[1] == '0'):
            
            numero_traduzido = numero_traduzido + 
        '''

porta = 3000
servidor = HTTPServer(('localhost', porta), Servidor)
print('Iniciando o servidor http://localhost:', porta)
servidor.serve_forever()