# 🔹 1. Primeiro código → Busca Gulosa com Fila (tipo BFS heurística)
# Estrutura:
# Usa deque → comportamento de fila (FIFO)
# Ordena os filhos por h(n) (heurística apenas)
# Estratégia:
# Sempre expande primeiro o nó com melhor heurística local
# MAS mantém estrutura de fila → mistura de BFS com heurística
# Fórmula usada:
# 𝑓
# (
# 𝑛
# )
# =
# ℎ
# (
# 𝑛
# )
# f(n)=h(n)
# Características:
# ❌ Ignora o custo real g(n)
# ✔ Simples e rápida
# ❌ Pode achar caminho não ótimo
# Intuição:

# "Vou sempre na direção que parece mais próxima do objetivo"

from collections import deque

# --- Estrutura de Rastreamento ---
class Rastreador:
    def __init__(self, vertice, anterior=None, custo_acumulado=0):
        self.vertice = vertice
        self.anterior = anterior
        self.custo_acumulado = custo_acumulado  # g(n)

# --- Classe de Heurística ---
class Heuristica:
    def __init__(self, pesos, conexoes):
        self.pesos = pesos  # h(n)
        self.adjacencias = conexoes  # {(origem, destino): custo_real}

    def get_ordenados(self, rastro_atual):
        no_pai = rastro_atual.vertice
        # Filtra vizinhos que partem do nó atual
        vizinhos = [v for (o, v) in self.adjacencias.keys() if o == no_pai]

        # ORDENAÇÃO PELA HEURÍSTICA h(n)
        return sorted(vizinhos, key=lambda v: self.pesos.get(v, 999))

# --- Algoritmo ---
def buscar_melhor_escolha(origem, meta, heuristica):
    fila = deque([Rastreador(origem)])
    visitados = {origem}

    while fila:
        atual = fila.popleft()
        print(f"Visitando: {atual.vertice} | Custo real acumulado: {atual.custo_acumulado}")

        if atual.vertice == meta:
            print(f"\n--- Meta encontrada! ---")
            print(f"Custo total da trajetória: {atual.custo_acumulado}")
            return True

        # O get_ordenados decide quem entra primeiro na fila baseado no peso (h)
        for filho in heuristica.get_ordenados(atual):
            if filho not in visitados:
                visitados.add(filho)

                # Busca o custo da aresta específica para atualizar o rastro
                custo_aresta = heuristica.adjacencias[(atual.vertice, filho)]
                novo_custo_real = atual.custo_acumulado + custo_aresta

                fila.append(Rastreador(filho, atual, novo_custo_real))
    return False

# --- Exemplo ---
meus_pesos_h = {'A': 10, 'B': 8, 'C': 5, 'D': 0} 
minhas_conexoes_custo = {
    ('A', 'B'): 5,
    ('A', 'C'): 20,
    ('B', 'D'): 10,
    ('C', 'D'): 2
}

h = Heuristica(meus_pesos_h, minhas_conexoes_custo)
buscar_melhor_escolha('A', 'D', h)