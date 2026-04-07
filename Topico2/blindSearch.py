#blind search é basicamente uma busca em vetor com um for

def blindSearch(lista, chave):
    i = 0
    while i < len(lista):
        if lista[i] == chave:
            return i
        i+=1
    return -1

lista = [1,2,3,4,5,6,7,8,9]

blindSearch(lista, 10)

