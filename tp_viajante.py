import os

import numpy as np
import pandas as pd
import folium
from folium.plugins import Search

data = pd.read_excel('TablaCapitales.xlsx', header=0)
ciudades = list(data)
distancias = data.to_numpy()
lat_lon = [[-34.6212767, -58.4145884],
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


def combinations(lista):  # Usado para armar una búsqueda exhaustiva.
    comb = [[]]
    cont = 0
    for x in lista:
        for r in comb:
            comb = comb + [r + [x]]
            cont = cont + 1
            print(cont)
    return comb


# combinations(ciudades)


def calcular_distancia_total():
    acum = 0
    for i in range(len(ciudades_visitadas) - 1):
        ciudad_origen = ciudades_visitadas[i]
        ciudad_final = ciudades_visitadas[i + 1]
        acum += distancias[ciudad_origen][ciudad_final]
    return acum


def visitar_ciudad_mas_cerana(partida):
    ciudades_ordenadas_desde_partida = np.argsort(distancias[partida])
    for final in ciudades_ordenadas_desde_partida:
        if final not in ciudades_visitadas:
            ciudades_visitadas.append(final)
            return final


# MENU

# for i in range(len(ciudades)):
#    print(i, " ", ciudades[i])
# partida = int(input("Ingrese número de ciudad inicial: "))
# print(ciudades[partida])

##


partida = 0

ciudades_visitadas = [partida]  # Creamos el arreglo ciudades_visitadas con partida como único elemento.

for i in range(len(ciudades)):
    partida = visitar_ciudad_mas_cerana(partida)

ciudades_visitadas.append(ciudades_visitadas[0])  # Se ingresa la ciudad inicial al final de las visitadas

print("Recorrido: ")
for i in ciudades_visitadas:
    print(ciudades[i])

print("Distancia total recorrida: ", calcular_distancia_total())


m = folium.Map(location=[-34.603722, -58.381592], zoom_start=4)  # Inicializa el mapa en Argentina.

for i in range(len(ciudades)):  # Hace marcadores en todas las capitales.
    folium.Marker(location=lat_lon[i], popup=ciudades[i]).add_to(m)

lat_lon_visitados = []
for i in ciudades_visitadas:  # Genera una lista con las latitudes y longitudes en el orden que se visitaron.
    lat_lon_visitados.append(lat_lon[i])
folium.PolyLine(locations=lat_lon_visitados, color='red').add_to(m)  # Genera las lineas del recorrido

m.save("index.html")
