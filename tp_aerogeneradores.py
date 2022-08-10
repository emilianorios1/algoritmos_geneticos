import random 
import numpy as np

filas = 10
columnas = 10

contador = 0
parque = np.zeros((filas, columnas)) # zeros inicializa una matriz con 0
for i in range(filas):
    for j in range(columnas):
        punto = random.randint(0, 1)
        if punto == 1 and contador < 25:
            parque[i][j] = punto
            contador+=1
print(parque)
