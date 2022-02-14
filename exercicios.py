#exec 1

class Votos():

    def __init__(self, total_eleitores, validos, brancos, nulos):
        self.total_eleitores = total_eleitores
        self.validos = validos
        self.brancos = brancos
        self.nulos   = nulos

    def percentual_validos(self):
        return self.validos / self.total_eleitores

    def percentual_brancos(self):
        return self.brancos / self.total_eleitores

    def percentual_nulos(self):
        return self.nulos / self.total_eleitores

total_eleitores = 1000
validos = 800
brancos = 150
nulos = 50

votos = Votos(total_eleitores, validos, brancos, nulos)    

#exerc 2

lista = [5, 3, 2, 4, 7, 1, 0, 6]

def bubble_sort(lista):
    tm_lista = len(lista)
    while tm_lista > 0:
        i = 0
        while i < tm_lista - 1:
            if lista[i] > lista[i + 1]:
                lista_temp = lista[i]
                lista[i] = lista[i + 1]
                lista[i + 1] = lista_temp
            i += 1
        tm_lista -= 1
    return lista

    
print(
    bubble_sort(lista)
)
# Uma forma melhor de fazer o sort é
lista2 = list(lista)
lista2.sort()
print(lista2)



#exec 3

def get_fatorial(numero):
    if numero <= 1:
        return 1
    return numero * get_fatorial(numero - 1)

print(
     get_fatorial(5)
)

#exerc 4

def multiplo(numero, multiplo):
    return numero % multiplo == 0

def soma(limite):
    soma = sum([ numero for numero in range(limite) if multiplo(numero, 3) or multiplo(numero, 5) ])
    return soma

print(
    soma(10) 
)