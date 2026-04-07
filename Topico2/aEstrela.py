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

    while abertos:
        # Extrai o nó de maior prioridade (menor f_n)
        atual = heapq.heappop(abertos)

        # Se alcançamos o objetivo, encerramos a busca
        if atual.vertice == meta:
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

    print("Caminho não encontrado.")
    return None



# --- Exemplo de Execução ---

# Pesos h(n): Estimativa de distância em linha reta até a meta 'D'
meus_pesos_h = {'A': 10, 'B': 8, 'C': 1, 'D': 0} 

# Conexões (Origem, Destino): Custo real da aresta g(n)
minhas_conexoes_custo = {
    ('A', 'B'): 5,
    ('A', 'C'): 10,
    ('B', 'D'): 10,
    ('C', 'D'): 2
}

h = Heuristica(meus_pesos_h, minhas_conexoes_custo)
buscar_a_estrela('A', 'D', h)