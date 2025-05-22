from collections import deque
import time
import networkx as nx
import matplotlib.pyplot as plt

# Definición del grafo
mapa_arrakis = {
    "Arrakeen": ["Sietch Tabr", "Oasis del Norte", "Campamento Fremen"],
    "Sietch Tabr": ["Arrakeen", "Oasis del Este", "Montaña de la Especia"],
    "Oasis del Norte": ["Arrakeen", "Campamento Fremen"],
    "Campamento Fremen": ["Arrakeen", "Oasis del Norte", "Oasis del Este"],
    "Oasis del Este": ["Sietch Tabr", "Campamento Fremen", "Zona Peligrosa"],
    "Montaña de la Especia": ["Sietch Tabr", "Zona Peligrosa"],
    "Zona Peligrosa": ["Oasis del Este", "Montaña de la Especia"]
}

# 1. BFS para encontrar la ruta más corta
def bfs_ruta_corta(origen, destino):
    cola = deque([[origen]])
    visitados = set()
    while cola:
        ruta = cola.popleft()
        nodo = ruta[-1]
        if nodo == destino:
            print(f"Ruta más corta desde {origen} hasta {destino}: {' -> '.join(ruta)}")
            print(f"Distancia total: {len(ruta)} nodos")
            return ruta
        if nodo not in visitados:
            for vecino in mapa_arrakis[nodo]:
                nueva_ruta = list(ruta)
                nueva_ruta.append(vecino)
                cola.append(nueva_ruta)
            visitados.add(nodo)
    return None

# 2. Verificar si el grafo es conexo usando DFS
def dfs_conexo(nodo, visitados):
    visitados.add(nodo)
    for vecino in mapa_arrakis[nodo]:
        if vecino not in visitados:
            dfs_conexo(vecino, visitados)

def verificar_conectividad():
    visitados = set()
    inicio = next(iter(mapa_arrakis))
    dfs_conexo(inicio, visitados)
    if len(visitados) == len(mapa_arrakis):
        print("El grafo es conexo.")
    else:
        print("El grafo NO es conexo.")

# 3. BFS para rutas seguras sin pasar por Zona Peligrosa
def bfs_rutas_seguras(origen, destino, peligro="Zona Peligrosa"):
    cola = deque([[origen]])
    rutas_seguras = []
    while cola:
        ruta = cola.popleft()
        nodo = ruta[-1]
        if nodo == destino:
            rutas_seguras.append(ruta)
        for vecino in mapa_arrakis[nodo]:
            if vecino not in ruta and vecino != peligro:
                nueva_ruta = list(ruta)
                nueva_ruta.append(vecino)
                cola.append(nueva_ruta)
    print(f"Rutas seguras desde {origen} hasta {destino} (evitando {peligro}):")
    for r in rutas_seguras:
        print(" -> ".join(r))
    return rutas_seguras

# 4. DFS para buscar Melange
def buscar_melange(origen):
    visitados = set()
    orden = []

    def dfs(nodo):
        if nodo not in visitados:
            visitados.add(nodo)
            orden.append(nodo)
            for vecino in mapa_arrakis[nodo]:
                dfs(vecino)

    dfs(origen)
    print("Orden de exploración de Melange desde Arrakeen:")
    print(" -> ".join(orden))
    return orden

# 5. Análisis de eficiencia
def analizar_eficiencia():
    print("\nAnálisis de eficiencia:")
    start = time.time()
    bfs_ruta_corta("Arrakeen", "Oasis del Norte")
    end = time.time()
    print(f"Tiempo BFS: {end - start:.6f} segundos")
    
    start = time.time()
    buscar_melange("Arrakeen")
    end = time.time()
    print(f"Tiempo DFS: {end - start:.6f} segundos")

    print("\n🔎 BFS es mejor para rutas más cortas.")
    print("🔎 DFS es mejor para recorrer todo el mapa.")

# 6. Visualización del grafo con matplotlib
def visualizar_grafo():
    G = nx.Graph()
    for nodo, vecinos in mapa_arrakis.items():
        for vecino in vecinos:
            G.add_edge(nodo, vecino)

    pos = nx.spring_layout(G, seed=42)  # layout para buena distribución
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='gold', edge_color='gray', node_size=1500, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos)
    plt.title("Mapa del Desierto de Arrakis")
    plt.show()

# Ejecución principal
if __name__ == "__main__":
    bfs_ruta_corta("Arrakeen", "Oasis del Norte")
    verificar_conectividad()
    bfs_rutas_seguras("Arrakeen", "Montaña de la Especia")
    buscar_melange("Arrakeen")
    analizar_eficiencia()
    visualizar_grafo()
