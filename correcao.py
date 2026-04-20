# IVAN DE ALMEIDA ASSIS	2310



# O objetivo deste teste é implementar o algoritmo de busca A (A-Estrela)* para encontrar a sequência mínima de movimentos necessária para resolver um quebra-cabeça deslizante de 2x2 (3-puzzle).

# Nesta implementação, cada estado do tabuleiro pode ser representado por uma string de 4 caracteres, onde o dígito 0 representa o espaço vazio.

# A correspondência entre a string e a grade 2x2 segue a ordem de leitura (da esquerda para a direita, de cima 
# para baixo): 
# ●  Índice 0: Superior Esquerdo 
# ●  Índice 1: Superior Direito 
# ●  Índice 2: Inferior Esquerdo 
# ●  Índice 3: Inferior Direito 
 
# 1  2 
# 3  0 

# Estado Objetivo: "1230"
 
# Regras de Movimentação 
# Um movimento consiste em trocar a posição do 0 com um vizinho adjacente. 

# Questão (2pts): CONCLUÍDO
# O aluno deve implementar o algoritmo  A* para encontrar o menor número de movimentos para chegar ao objetivo partindo do seguinte estado inicial: 

# 2  3 
# 1  0 
#     Estado Inicial: "2310"

#  Para isto deverá: 
# ○  Criar o grafo(conexoes) do problema completo, contendo todos os caminhos (0.5pts); CONCLUÍDO
# ○  Criar as heurísticas para o problema(0.5pts). CONCLUÍDO

# Insira um comentário no código indicando qual foi a heurística escolhida. CONCLUÍDO
 
#   Saída (Obrigatória):  (1.0pts)
# ○  Menor caminho: Imprimir a sequência exata de estados (strings) desde a entrada até o objetivo. CONCLUÍDO
# ○  Custo Total: Número de movimentos (final). CONCLUÍDO
 
# Ao final o aluno deverá enviar apenas o arquivo .py no Vianna Virtual  

import heapq
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(order=True)
class Rastreador:
    """
    Armazena o estado de exploração de um nó.
    O parâmetro order=True permite que o heapq ordene os objetos pelo campo 'f_n'.
    """
    f_n: float  # Prioridade total: g(n) + h(n)
    vertice: Any = field(compare=False)
    anterior: Optional["Rastreador"] = field(default=None, compare=False)
    g_n: float = field(default=0.0, compare=False)  # Custo real acumulado


class Heuristica:
    """
    Gerencia o conhecimento sobre o mapa, incluindo custos de conexão
    e a estimativa (peso) de cada vértice até o objetivo.
    """
    def __init__(self, pesos, conexoes):
        self.pesos = pesos  
        self.adjacencias = conexoes  

    def obter_vizinhos(self, no_pai):
        """Retorna uma lista de tuplas (vizinho, custo_da_aresta)."""
        return [(v, c) for (o, v), c in self.adjacencias.items() if o == no_pai]


def buscar_a_estrela(origem, meta, heuristica):
    """
    Executa a busca A* para encontrar o caminho com menor custo total.
    Combina a busca de custo uniforme com a busca gananciosa.
    """
    # Fila de prioridade para explorar sempre o nó com menor f(n)
    abertos = []

    # Registro do menor custo real (g_n) encontrado para cada vértice
    melhores_g = {origem: 0.0}

    # Inicialização com o nó de origem
    h_inicial = heuristica.pesos.get(origem, 999)
    no_inicial = Rastreador(f_n=h_inicial, vertice=origem, g_n=0.0)

    heapq.heappush(abertos, no_inicial)
    contadorNosExpandidos = 0

    while abertos:
        # Extrai o nó de maior prioridade (menor f_n)
        atual = heapq.heappop(abertos)
        contadorNosExpandidos+=1
        
        print(f"Custo atual: {atual.g_n}, Estimativa restante: {atual.f_n - atual.g_n}, Vertice: {atual.vertice}")

        # Se alcançamos o objetivo, encerramos a busca
        if atual.vertice == meta:
            print("______________________________________")
            print(f"Custo acumulado: {atual.g_n}")
            numeroMovimentosFinal = atual.g_n
            caminho = []
            while atual is not None:
                caminho.append(atual.vertice)
                atual = atual.anterior
            
            caminho.reverse()
            print(f"O caminho foi: {caminho}")
            print()
            print(f"O numero de nós expandidos foi de {contadorNosExpandidos}")
            print()
            print(f"O numero de movimentos foi de {numeroMovimentosFinal}")

            return True

        # Exploração dos vizinhos do vértice atual
        for vizinho, custo_aresta in heuristica.obter_vizinhos(atual.vertice):
            # Cálculo do custo real para chegar ao vizinho por este caminho
            tentativa_g = atual.g_n + custo_aresta

            # Se este caminho for melhor que qualquer um encontrado anteriormente
            if tentativa_g < melhores_g.get(vizinho, float('inf')):
                melhores_g[vizinho] = tentativa_g
                h_n = heuristica.pesos.get(vizinho, 999)

                # f(n) = g(n) + h(n)
                novo_no = Rastreador(
                    f_n=tentativa_g + h_n,
                    vertice=vizinho,
                    anterior=atual,
                    g_n=tentativa_g
                )
                heapq.heappush(abertos, novo_no)

    print("Caminho nao encontrado.")
    return None


# --- Exemplo de Execução ---

#QUESTAO 2: Insira um comentário no codigo indicando qual foi a heúrística escolhida:

            #Resposta: Manhattan. É aquela que o quebra cabeca é descontruido todo e é contado quantos movimentos você precisa pra cada peca chegar no estado ideal a partir do quebra cabeças desmontado, usamos ela em aula.
            
            #o 0 no caso e espaco vazio e nao peca, entao nao conta ele
meus_pesos_h = {
    "2310": 4,
    "2301": 5,
    "0321": 4,
    "3021": 3,
    "3120": 2,
    "3102": 2,
    "0132": 2,
    "1032": 1,
    "1230": 0,
    "0213": 3,
    "1203": 1,
    "2013": 3
}

# Conexões (Origem, Destino): Custo real da aresta g(n)

#ESTADO INICIAL == 2310
minhas_conexoes_custo = {
    ('2310', '2013'): 1,
    ('2310', '2301'): 1,

    ('2013', '2310'): 1,
    ('2013', '0213'): 1,

    ('2301', '2310'): 1,
    ('2301', '0321'): 1,

    ('0321', '2301'): 1,
    ('0321', '3021'): 1,

    ('3021', '0321'): 1,
    ('3021', '3120'): 1,

    ('3120', '3021'): 1,
    ('3120', '3102'): 1,

    ('3102', '3120'): 1,
    ('3102', '0132'): 1,

    ('0132', '3102'): 1,
    ('0132', '1032'): 1,

    ('1032', '0132'): 1,
    ('1032', '1230'): 1,

    ('0213', '2013'): 1,
    ('0213', '1203'): 1,

    ('1203', '0213'): 1,
    ('1203', '1230'): 1,

    ('1230', '1032'): 1,
    ('1230', '1203'): 1
}

h = Heuristica(meus_pesos_h, minhas_conexoes_custo)
buscar_a_estrela('2310', '1230', h)