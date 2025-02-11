import networkx as nx
import matplotlib.pyplot as plt
import random

# Crear un grafo dirigido
G = nx.DiGraph()

# Número de clientes y vehículos
num_clientes = 10
num_vehiculos = 3

# Capacidad de los vehículos (heterogénea)
capacidad_vehiculos = {0: 100, 1: 150, 2: 120}  # Capacidad de cada vehículo

# Demanda de los clientes (aleatoria)
demandas = {i: random.randint(5, 20) for i in range(1, num_clientes + 1)}

# Tiempos de servicio (aleatorios)
tiempos_servicio = {i: random.randint(5, 15) for i in range(1, num_clientes + 1)}

# Ventanas de tiempo (aleatorias)
ventanas_tiempo = {
    i: (random.randint(8, 10) * 60,  # Tiempo más temprano (en minutos desde la medianoche)
    random.randint(12, 14) * 60)    # Tiempo más tardío (en minutos desde la medianoche)
    for i in range(1, num_clientes + 1)
}

# Añadir nodos (depósito y clientes)
nodes = [0] + list(range(1, num_clientes + 1))  # 0 es el depósito
G.add_nodes_from(nodes)

# Generar rutas aleatorias para cada vehículo
vehiculos = {}
capacidad_usada = {k: 0 for k in range(num_vehiculos)}  # Capacidad usada por cada vehículo
tiempo_actual = {k: 0 for k in range(num_vehiculos)}    # Tiempo actual de cada vehículo

for k in range(num_vehiculos):
    vehiculos[k] = [0]  # Cada vehículo comienza en el depósito
    clientes_disponibles = list(range(1, num_clientes + 1))
    while clientes_disponibles:
        cliente = random.choice(clientes_disponibles)
        if (capacidad_usada[k] + demandas[cliente] <= capacidad_vehiculos[k] and
            tiempo_actual[k] + tiempos_servicio[cliente] <= ventanas_tiempo[cliente][1]):
            vehiculos[k].append(cliente)
            capacidad_usada[k] += demandas[cliente]
            tiempo_actual[k] += tiempos_servicio[cliente]
            clientes_disponibles.remove(cliente)
        else:
            break
    vehiculos[k].append(0)  # Cada vehículo termina en el depósito

# Añadir aristas (rutas de los vehículos) con colores
colores = ['red', 'blue', 'green', 'purple', 'orange']  # Colores para cada vehículo
edge_colors = []
for k in vehiculos:
    ruta = vehiculos[k]
    for i in range(len(ruta) - 1):
        G.add_edge(ruta[i], ruta[i + 1])
        edge_colors.append(colores[k])

# Posiciones de los nodos para el gráfico
pos = nx.spring_layout(G, seed=42)  # Layout para organizar los nodos

# Dibujar el grafo
plt.figure(figsize=(14, 10))
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# Dibujar las aristas con colores según el vehículo
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, width=2)

# Añadir etiquetas de carga y tiempo
labels = {0: "Depósito"}
for i in range(1, num_clientes + 1):
    labels[i] = (
        f"Cliente {i}\n"
        f"Demanda: {demandas[i]}\n"
        f"Ventana: [{ventanas_tiempo[i][0]//60}:{ventanas_tiempo[i][0]%60:02d}, "
        f"{ventanas_tiempo[i][1]//60}:{ventanas_tiempo[i][1]%60:02d}]"
    )

nx.draw_networkx_labels(G, pos, labels, font_size=8)

# Crear una leyenda para los vehículos
legend_labels = [f"Vehículo {k} (Capacidad: {capacidad_vehiculos[k]}, Usada: {capacidad_usada[k]})" for k in range(num_vehiculos)]
legend_colors = [colores[k] for k in range(num_vehiculos)]
patches = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_colors]
plt.legend(patches, legend_labels, loc='upper right', fontsize=10)

# Guardar el gráfico como imagen
plt.savefig("vrptw_extended_graph.png", format="PNG", dpi=300)

# Mostrar el gráfico
plt.title("VRPTW Extendido - Rutas de Vehículos con Cargas y Tiempos", fontsize=16)
plt.show()