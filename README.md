# NumerosExtensos

Depend�ncias
Python 3.7
biblioteca requests

Execucao:

Ap�s a instala��o da biblioteca requests com "pip install requests"
Executar o servidor com "python server.py"
Ap�s o servidor ficara ouvindo na porta 3000, respondendo a comando curl.
O n�mero a ser traduzido pode ser passado com o commando "curl http://localhost:3000/#", onde # pode ser um n�mero entre [-99999, 99999]
Respondendo com um json com a chave "extenso": "menos novecentos e noventa e nove"

Tamb�m pode ser utilizado a classe client, passando como argumento o n�mero a ser traduzido