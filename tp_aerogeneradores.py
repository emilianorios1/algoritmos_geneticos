import random
import numpy as np

filas = 10
columnas = 10  # cada punto son 100 metros cuadrados (1 hect)
poblacion = 10
vel_viento = 5
cant_max_generadores = 25
probabilidad_crossover = 0.8
probabilidad_mutacion = 0.2
cant_elitismo = 2
elitismo = False
cant_torneo = 2
metodo_seleccion = 'ruleta'
ciclos = 10

# variables funcion objetivo
coef_ind_axial = (1 / 3)  # apunte como a
coef_sustent = 0.888
velocidad_inicial_viento = 20
rugosidad_terreno = 0.005  # Z0
radio_molino = 23.5
altura_buje = 50  # Z
coeficiente_arrastre = 1 / (2 * np.log(altura_buje / rugosidad_terreno))  # alfa
velocidades = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
potencias = [0, 4, 43, 96, 166, 252, 350, 450, 538, 600, 635, 651, 657, 659, 660, 660, 660, 660, 660, 660, 660, 660,
             660, 660, 660]
distancia_entre_molinos = 100


def crear_parque_inicial():
    m = np.zeros((filas, columnas))
    cont = 0
    cant_generadores = random.randrange(cant_max_generadores + 1)
    while cont < cant_generadores:
        x = random.randrange(filas)
        y = random.randrange(columnas)
        if m[x][y] == 0:
            m[x][y] = 1
            cont = cont + 1
    return m


def calcular_potencia_generador(parque, i, j):
    if parque[i][j] == 1:
        estela = False
        for k in range(i):
            if parque[k][j] == 1:
                velocidad_efecto_estela = round(
                    velocidad_inicial_viento * (1 - (2 * coef_ind_axial) / np.square(
                        1 + (coeficiente_arrastre * (distancia_entre_molinos * (i - k)) / radio_molino))))
                estela = True
        if estela:
            indice = velocidades.index(velocidad_efecto_estela)
        else:
            indice = velocidades.index(velocidad_inicial_viento)
        return potencias[indice]
    else:
        return 0

def calcular_potencia_parque(parque):
    acum_potencia = 0
    for i in range(filas):
        for j in range(columnas):
            acum_potencia += calcular_potencia_generador(parque, i, j)
    return acum_potencia

def calcular_potencia_fila(parque, i):
    acum_potencia = 0
    for j in range(columnas):
        acum_potencia += calcular_potencia_generador(parque, i, j)
    return acum_potencia

def calcular_potencia_columna(parque, j):
    acum_potencia = 0
    for i in range(filas):
        acum_potencia += calcular_potencia_generador(parque, i, j)
    return acum_potencia


def cargar_tablas():
    for i in range(poblacion):
        parques_objetivo.append(calcular_potencia_parque(parques_actuales[i]))
    for i in range(poblacion):
        parques_fitness.append(parques_objetivo[i] / sum(parques_objetivo))


def ruleta():
    ## if (si la prob fitness es menor a 0.01) redondearla para que sea por lo menos 0.01
    limite = random.uniform(0, 1)  ##Número real de 0 a 1 inclusive.
    acum = 0
    i = 0
    ## sumamos los fitness de todos los cromosomas,
    while acum < limite:
        acum += parques_fitness[i]
        parque = parques_actuales[i]
        i = i + 1
    return parque.copy()


def torneo():
    torneo_fitness = []
    torneo_binario = []
    for i in range(cant_torneo):
        parque_index = random.randrange(poblacion)
        torneo_fitness.append(parques_fitness[parque_index])
        torneo_binario.append(parques_actuales[parque_index])
    return torneo_binario[np.argmax(torneo_fitness)].copy()


def mutar(parque):
    x = random.randrange(filas)
    y = random.randrange(columnas)
    if parque[x][y] == 1:
        parque[x][y] = 0
    else:
        parque[x][y] = 1
    return parque.copy()


def crossover(parque1, parque2):
    hijo1 = np.zeros((filas, columnas))
    hijo2 = np.zeros((filas, columnas))
    for i in range(filas):
        fila1 = calcular_potencia_fila(parque1, i)  # suma de filas
        fila2 = calcular_potencia_fila(parque2, i)
        if fila1 > fila2:
            hijo1[i] = parque1[i]
        else:
            hijo1[i] = parque2[i]
    for j in range(columnas):
        columna1 = calcular_potencia_columna(parque1, j)  # suma de columnas
        columna2 = calcular_potencia_columna(parque2, j)
        if columna1 > columna2:
            hijo2[j] = parque1.transpose()[j]
        else:
            hijo2[j] = parque2.transpose()[j]
        hijo2 = hijo2.transpose()

    return hijo1.copy(), hijo2.copy()


def cargar_nueva_generacion():
    flag = False
    while not flag:
        if metodo_seleccion == 'ruleta':
            parque1 = ruleta()
            parque2 = ruleta()
        else:
            parque1 = torneo()
            parque2 = torneo()
        if random.uniform(0, 1) < probabilidad_crossover:
            parque1, parque2 = crossover(parque1, parque2)
        if random.uniform(0, 1) < probabilidad_mutacion:
            parque1 = mutar(parque1)
            parque2 = mutar(parque2)
        if np.sum(parque1) <= cant_max_generadores and np.sum(parque2) <= cant_max_generadores:
            # Si alguno de mis nuevos hijos tiene mas aerogeneradores de los posibles los descarto.
            parques_nuevos.append(parque1.copy())
            parques_nuevos.append(parque2.copy())
            flag = True


parques_nuevos = []
maximos_parque = []
maximos_objetivo = []
minimos_objetivo = []
promedios_objetivo = []

for i in range(poblacion):
    parques_nuevos.append(crear_parque_inicial())

for i in range(ciclos):
    parques_actuales = parques_nuevos
    parques_objetivo = []
    parques_fitness = []
    cargar_tablas()

    maximos_parque.append(parques_actuales[np.argmax(parques_objetivo)])
    maximos_objetivo.append(np.max(parques_objetivo))
    minimos_objetivo.append(np.min(parques_objetivo))
    promedios_objetivo.append(np.average(parques_objetivo))

    parques_nuevos = []
    if elitismo:
        # Se cargan los cromosomas que pasan por elitismo, según su fitness se consigue su índice en la lista,
        # a partir de eso se busca en el binario
        for i in range(cant_elitismo):
            parques_nuevos.append(parques_actuales[parques_fitness.index(sorted(parques_fitness, reverse=True)[i])])
        cant_cargas = int((poblacion - cant_elitismo) / 2)
    else:
        cant_cargas = int(poblacion / 2)
    for i in range(cant_cargas):
        cargar_nueva_generacion()

for i in range(ciclos):
    print("generacion ", i)
    print("max parque: ", maximos_parque[i])
    print("cant aerogeneradores", np.sum(maximos_parque[i]))
    print("max objetivo: ", maximos_objetivo[i])
    print("min objetivo: ", minimos_objetivo[i])
