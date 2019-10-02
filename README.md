# NumerosExtensos

Dependências
Python 3.7
biblioteca requests

Execucao:

Após a instalação da biblioteca requests com "pip install requests"
Executar o servidor com "python server.py"
Após o servidor ficara ouvindo na porta 3000, respondendo a comando curl.
O número a ser traduzido pode ser passado com o commando "curl http://localhost:3000/#", onde # pode ser um número entre [-99999, 99999]
Respondendo com um json com a chave "extenso": "menos novecentos e noventa e nove"

Também pode ser utilizado a classe client, passando como argumento o número a ser traduzido