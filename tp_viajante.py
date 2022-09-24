
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader as sf
from cartopy.feature import ShapelyFeature as cfeature


#El archivo shp lo pueden encontrar en la página del Instituto Geográfico Nacional (IGN)
fname = 'provincia.shp'

fig, ax = plt.subplots( 1, 1, subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=[12,14]  )
shape_feature = cfeature(sf(fname).geometries(), ccrs.PlateCarree(), edgecolor='black')
ax.add_feature(shape_feature, facecolor= 'none')

#Defino los ejes (lon min y max, lat min y max)
ax.set_extent([-76, -53, -57, -20])

data = pd.read_excel('TablaCiudades.xlsx', header=0)
ciudades = list(data)
distancias = data.to_numpy()


def combinations(lista): # Usado para armar una búsqueda exhaustiva.
    comb = [[]]
    cont = 0
    for x in lista:
        for r in comb:
            comb = comb + [r+[x]]
            cont = cont+1
            print(cont)
    return comb

# combinations(ciudades)


def calcular_distancia_total():
    acum = 0
    for i in range(len(ciudades_visitadas) - 1):
        ciudad_origen = ciudades_visitadas[i]
        ciudad_final = ciudades_visitadas[i+1]
        acum += distancias[ciudad_origen][ciudad_final]
    return acum


def visitar_ciudad_mas_cerana(partida):
    ciudades_ordenadas_desde_partida = np.argsort(distancias[partida])
    for final in ciudades_ordenadas_desde_partida:
        if final not in ciudades_visitadas:
            ciudades_visitadas.append(final)
            return final


# MENU

for i in range(len(ciudades)):
    print(i, " ", ciudades[i])
partida = int(input("Ingrese número de ciudad inicial: "))
print(ciudades[partida])

##


#partida = 4

ciudades_visitadas = [partida]  # Creamos el arreglo ciudades_visitadas con partida como único elemento.

for i in range(len(ciudades)):
    partida = visitar_ciudad_mas_cerana(partida)

ciudades_visitadas.append(ciudades_visitadas[0])  # Se ingresa la ciudad inicial al final de las visitadas

print("Recorrido: ")
for i in ciudades_visitadas:
    print(ciudades[i])

print("Distancia total: ", calcular_distancia_total())

