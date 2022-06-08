volumenes = [150, 325, 600, 805, 430, 1200, 770, 60, 930, 353]

valores = [20, 40, 50, 36, 25, 64, 54, 18, 46, 28]

volumen_mochila = 4200

#division = []
#for i in range(len(valores)):
#  division.append(volumenes[i] / valores[i])

#Crea toda las combinaciones posibles, empieza con el arreglo vacío y uno por uno agrega elementos
#una vez que se agrega un elemento se añade ese elemento a todas las combinaciones anteriores calculadas dandoles el valor r
#y agregándole el proximo elemento
#Ej: empieza en c=[[]] -> 
# c= [[],[0]] -> 
# c= [[],[0],[1]]
# c= [[],[0],[1],[0, 1]] -> 
# c= [[], [0], [1], [0, 1], [2]] -> 
#                          //^ acá se suma [] + [2]//
#
# c= [[], [0], [1],[0, 1], [2], [0,2]] -> 
# c= [[], [0], [1],[0, 1], [2], [0,2], [1,2]]  -> 
# c= [[], [0], [1],[0, 1], [2], [0,2], [1,2], [0,1,2]]  -> 
#                                            //^ acá se suma [0,1] + [2]//
def combinations():
  c = [[]]
  for x in range(len(valores)):
      for r in c:
        c= c + [r+[x]]
  return c
combinaciones = combinations()