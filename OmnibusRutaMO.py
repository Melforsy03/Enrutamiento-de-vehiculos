import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import permutations

# **1️⃣ Generar Datos del Problema VRPTW (Ahora con más vehículos y clientes)**
num_clientes = 8  # Más clientes para mayor complejidad
num_vehiculos = 3  # Múltiples vehículos
clientes = list(range(1, num_clientes + 1))
nodos = [0] + clientes  # Nodo 0 es el depósito

# Generar costos aleatorios entre nodos
costo = {(i, j): np.random.randint(10, 100) for i in nodos for j in nodos if i != j}

# Ventanas de tiempo aleatorias
ventana_tiempo = {i: (np.random.randint(1, 10), np.random.randint(20, 40)) for i in clientes}

# Demandas aleatorias y capacidad de cada vehículo
demanda_cliente = {i: np.random.randint(5, 30) for i in clientes}
capacidad_vehiculo = 100

# Mostrar datos generados
print("\n📌 Costos de viaje:", costo)
print("📌 Ventanas de tiempo:", ventana_tiempo)
print("📌 Demandas de clientes:", demanda_cliente)

# **2️⃣ Algoritmo Mejorado para encontrar rutas óptimas por vehículo (Simulación de Simplex con Múltiples Vehículos)**
def calcular_costo(ruta):
    return sum(costo[ruta[i], ruta[i+1]] for i in range(len(ruta)-1))

# Dividir clientes en grupos para cada vehículo (Estrategia simple)
clientes_por_vehiculo = np.array_split(clientes, num_vehiculos)

rutas_vehiculos = []
costos_vehiculos = []

for vehiculo, clientes_asignados in enumerate(clientes_por_vehiculo):
    mejor_ruta = None
    mejor_costo = float('inf')

    for perm in permutations(clientes_asignados):
        ruta_actual = [0] + list(perm) + [0]  # Empieza y termina en el depósito
        costo_ruta = calcular_costo(ruta_actual)

        if costo_ruta < mejor_costo:
            mejor_costo = costo_ruta
            mejor_ruta = ruta_actual

    rutas_vehiculos.append(mejor_ruta)
    costos_vehiculos.append(mejor_costo)

# **3️⃣ Visualización Mejorada con Múltiples Rutas y Vehículos**
fig, ax = plt.subplots(figsize=(10, 6))
G = nx.DiGraph()

# Colores diferentes para cada vehículo
colores = ['blue', 'red', 'green', 'purple', 'orange', 'pink']

for i, ruta in enumerate(rutas_vehiculos):
    edges = [(ruta[j], ruta[j+1]) for j in range(len(ruta)-1)]
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)
    labels = {edge: costo[edge] for edge in edges}
    
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=1500, edge_color=colores[i], width=2.5, font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

plt.title("🚛 Solución VRPTW - Múltiples Vehículos con Simulación de Simplex")
plt.show()

# **4️⃣ Algoritmo de Ramificación y Acotación Mejorado para múltiples vehículos**
def branch_and_bound(ruta_actual, costo_actual, nodos_restantes):
    global mejor_ruta_bb, mejor_costo_bb

    if not nodos_restantes:
        costo_actual += costo[ruta_actual[-1], 0]
        if costo_actual < mejor_costo_bb:
            mejor_costo_bb = costo_actual
            mejor_ruta_bb = ruta_actual + [0]
        return

    for siguiente in nodos_restantes:
        nuevo_costo = costo_actual + costo[ruta_actual[-1], siguiente]
        if nuevo_costo < mejor_costo_bb:
            branch_and_bound(ruta_actual + [siguiente], nuevo_costo, [n for n in nodos_restantes if n != siguiente])

# Ejecutar B&B por cada vehículo
mejor_rutas_bb = []
mejor_costos_bb = []

for vehiculo, clientes_asignados in enumerate(clientes_por_vehiculo):
    mejor_ruta_bb = []
    mejor_costo_bb = float('inf')

    branch_and_bound([0], 0, list(clientes_asignados))

    mejor_rutas_bb.append(mejor_ruta_bb)
    mejor_costos_bb.append(mejor_costo_bb)

# **5️⃣ Visualización Mejorada de Branch and Bound**
fig, ax = plt.subplots(figsize=(10, 6))
G_bb = nx.DiGraph()

for i, ruta in enumerate(mejor_rutas_bb):
    edges_bb = [(ruta[j], ruta[j+1]) for j in range(len(ruta)-1)]
    G_bb.add_edges_from(edges_bb)

    pos_bb = nx.spring_layout(G_bb)
    labels_bb = {edge: costo[edge] for edge in edges_bb}

    nx.draw(G_bb, pos_bb, with_labels=True, node_color='lightgray', node_size=1500, edge_color=colores[i], width=2.5, font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G_bb, pos_bb, edge_labels=labels_bb, ax=ax)

plt.title("🚚 Solución VRPTW - Múltiples Vehículos con Branch & Bound")
plt.show()

# **6️⃣ Guardar los resultados en un archivo**
with open("resultado_vrptw_exposicion.txt", "w") as file:
    file.write("Solución Simulación de Simplex con Múltiples Vehículos:\n")
    for i, ruta in enumerate(rutas_vehiculos):
        file.write(f"Vehículo {i+1}: Ruta: {' -> '.join(map(str, ruta))}, Costo: {costos_vehiculos[i]}\n")

    file.write("\nSolución Branch & Bound con Múltiples Vehículos:\n")
    for i, ruta in enumerate(mejor_rutas_bb):
        file.write(f"Vehículo {i+1}: Ruta: {' -> '.join(map(str, ruta))}, Costo: {mejor_costos_bb[i]}\n")

print("\n📂 Resultados exportados a 'resultado_vrptw_exposicion.txt'")
