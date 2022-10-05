import numpy as np
import pandas as pd
import folium
import random

print("1 - Heuristica - Elegir partida ")
print("2 - Heuristica - Mejor recorrido")
print("3 - Genetico")
modo = int(input("Ingrese selección: "))

data = pd.read_excel('TablaCapitales.xlsx', header=0)
ciudades = list(data)
distancias = data.to_numpy()
lat_lon = [[-34.6212767, -58.4145884],  # Mapeo manual de las latitudes y longitudes de cada provincia.
           [-31.3994342, -64.2643837],
           [-27.4862473, -58.8274061],
           [-26.1721517, -58.2299893],
           [-34.9205233, -57.9881897],
           [-29.4142924, -66.8907965],
           [-32.883334, -68.8760287],
           [-38.9412294, -68.1504201],
           [-31.7472984, -60.5867216],
           [-27.396305, -55.9595352],
           [-43.2988158, -65.1206438],
           [-27.4606431, -59.0671039],
           [-51.6264434, -69.3067685],
           [-28.4645296, -65.8101793],
           [-26.8328546, -65.2576131],
           [-24.2053356, -65.3405747],
           [-24.7960685, -65.5006685],
           [-31.5317743, -68.5501862],
           [-33.297652, -66.3446851],
           [-31.6181226, -60.7780156],
           [-36.6193822, -64.336255],
           [-27.8017104, -64.3020677],
           [-54.8068581, -68.3378226],
           [-40.8250227, -63.0176492]
           ]


def graficar_mapa(recorrido):
    m = folium.Map(location=[-34.603722, -58.381592], zoom_start=4)  # Inicializa el mapa en Argentina.

    for i in range(len(ciudades)):  # Hace marcadores en todas las capitales.
        folium.Marker(location=lat_lon[i], popup=ciudades[i]).add_to(m)

    lat_lon_visitados = []
    for i in recorrido:  # Genera una lista con las latitudes y longitudes en el orden que se visitaron.
        lat_lon_visitados.append(lat_lon[i])
    lat_lon_visitados.append(lat_lon[recorrido[0]])
    folium.PolyLine(locations=lat_lon_visitados, color='red').add_to(m)  # Genera las líneas del recorrido

    m.save("index.html")


def calcular_distancia_total(recorrido):  # Es también la función objetivo en el algoritmo genético.
    acum = 0
    for i in range(len(recorrido) - 1):
        ciudad_origen = recorrido[i]
        ciudad_destino = recorrido[i + 1]
        acum += distancias[ciudad_origen][ciudad_destino]
    ciudad_origen = recorrido[-1]  # Es el ultimo elemento
    ciudad_destino = recorrido[0]  # Es el primer elemento
    acum += distancias[ciudad_origen][ciudad_destino]
    return acum


def print_recorrido(recorrido):
    print("Distancia reocorrida: ", calcular_distancia_total(recorrido))
    print("Recorrido: ")
    for i in recorrido:
        print("   ", ciudades[i])
    print("   ", ciudades[recorrido[0]])


############ INICIO HEURISTICA
if modo == 1 or modo == 2:
    # MENU
    def heuristica(partida):
        def visitar_ciudad_mas_cercana(partida):
            ciudades_ordenadas_desde_partida = np.argsort(distancias[partida])
            for final in ciudades_ordenadas_desde_partida:
                if final not in ciudades_visitadas:
                    ciudades_visitadas.append(final)
                    return final

        ciudades_visitadas = [partida]  # Creamos el arreglo ciudades_visitadas con partida como único elemento.

        for i in range(len(ciudades)):
            partida = visitar_ciudad_mas_cercana(partida)

        return ciudades_visitadas


    if modo == 1:
        for i in range(len(ciudades)):
            print(i, " ", ciudades[i])
        partida = int(input("Ingrese número de ciudad inicial: "))
        print(ciudades[partida])
        recorrido_heuristico = heuristica(partida)

    if modo == 2:
        minimo_distancia = 999999999
        for i in range(len(ciudades)):
            aux_recorrido = heuristica(i)
            if minimo_distancia > calcular_distancia_total(aux_recorrido):
                minimo_distancia = calcular_distancia_total(aux_recorrido)
                recorrido_heuristico = aux_recorrido

    graficar_mapa(recorrido_heuristico)
    print_recorrido(recorrido_heuristico)

############ FIN HEURISTICA


############ INICIO GENETICO

if modo == 3:

    poblacion = 50
    ciclos = 200
    cant_elitismo = 2
    elitismo = True
    cant_torneo = 2
    probabilidad_crossover = 0.8
    probabilidad_mutacion = 0.2


    def ruleta():
        ## if (si la prob fitness es menor a 0.01) redondearla para que sea por lo menos 0.01
        limite = random.uniform(0, 1)  ##Número real de 0 a 1 inclusive.
        acum = 0
        i = 0
        ## sumamos los fitness de todos los cromosomas,
        while acum < limite:
            acum += recorridos_fitness[i]
            recorrido = recorridos_actuales[i]
            i = i + 1
        return recorrido.copy()


    def crossover(padre1, padre2):
        hijo = [99 for element in range(len(ciudades))]
        hijo[0] = padre1[0]
        indice_abajo = 0
        while 0 == 0:
            valor = padre2[indice_abajo]
            indice_arriba = padre1.index(valor)
            if indice_arriba == 0:
                break
            hijo[indice_arriba] = padre1[indice_arriba]
            indice_abajo = indice_arriba
        for i in range(len(ciudades)):
            if hijo[i] == 99:
                hijo[i] = padre2[i]
        return hijo.copy()


    def mutar(recorrido):
        g1 = random.randrange(len(recorrido))
        g2 = random.randrange(len(recorrido))
        recorrido[g1], recorrido[g2] = recorrido[g2], recorrido[g1]
        return recorrido.copy()


    def cargar_nueva_generacion():
        recorrido1 = ruleta()
        recorrido2 = ruleta()
        if random.uniform(0, 1) < probabilidad_crossover:
            aux_1 = crossover(recorrido1, recorrido2)
            aux_2 = crossover(recorrido2, recorrido1)
            recorrido1 = aux_1.copy()
            recorrido2 = aux_2.copy()
        if random.uniform(0, 1) < probabilidad_mutacion:
            recorrido1 = mutar(recorrido1)
            recorrido2 = mutar(recorrido2)
        nueva_generacion.append(recorrido1)
        nueva_generacion.append(recorrido2)


    # DECLARACIÓN DE ARREGLOS
    nueva_generacion = []
    maximos_recorrido = []
    # CARGA INICIAL
    for i in range(poblacion):
        nueva_generacion.append(random.sample(list(range(len(ciudades))), len(ciudades)))
    # FIN CARGA INICIAL
    for i in range(ciclos):
        # CARGAMOS LA GENERACION NUEVA
        recorridos_actuales = nueva_generacion.copy()
        recorridos_objetivo = []
        recorridos_fitness = []
        for i in range(poblacion):
            recorridos_objetivo.append(1 / calcular_distancia_total(recorridos_actuales[i]))
        for i in range(poblacion):
            recorridos_fitness.append(recorridos_objetivo[i] / sum(recorridos_objetivo))
        # FIN CARGA DE GENERACION NUEVA

        maximos_recorrido.append(recorridos_actuales[np.argmax(recorridos_objetivo)])

        nueva_generacion = []
        if elitismo:
            # Se cargan los cromosomas que pasan por elitismo, según su fitness se consigue su índice en la lista,
            # a partir de eso se busca en el binario
            for i in range(cant_elitismo):
                nueva_generacion.append(
                    recorridos_actuales[recorridos_fitness.index(sorted(recorridos_fitness, reverse=True)[i])])
            cant_cargas = int((poblacion - cant_elitismo) / 2)
        else:
            cant_cargas = int(poblacion / 2)
        for i in range(cant_cargas):
            cargar_nueva_generacion()

    print("Recorrido número: ", ciclos)
    print_recorrido(maximos_recorrido[ciclos - 1])
    graficar_mapa(maximos_recorrido[ciclos - 1])
