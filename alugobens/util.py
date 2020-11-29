import string
from random import choice

def gerarHash(tamanho):
    valores = string.ascii_letters
    valores += string.digits

    codigo = ""

    for i in range(tamanho):
        codigo += choice(valores)

    return codigo