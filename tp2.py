volumenes = [150, 325, 600, 805, 430, 1200, 770, 60, 930, 353]

valores = [20, 40, 50, 36, 25, 64, 54, 18, 46, 28]

volumen_mochila = 4200

#division = []
#for i in range(len(valores)):
#  division.append(volumenes[i] / valores[i])


def combinations():
  c = [[]]
  for x in range(len(valores)):
      for r in c:
        c= c + [r+[x]]
  return c
combinaciones = combinations()


acum_volumenes = 0
max_valor = 0
n_mejor = 0

for i in range(len(combinaciones)):
  acum_valores = 0
  acum_volumenes = 0

  for j in range(len(combinaciones[i])):
    acum_valores = acum_valores + valores[combinaciones[i][j]]
    acum_volumenes = acum_volumenes + volumenes[combinaciones[i][j]]
  
  if(acum_valores > max_valor and acum_volumenes < volumen_mochila):
    n_mejor = i
    max_valor = acum_valores

acum_valores = 0
acum_volumenes = 0

print("La mejor combinación es ", n_mejor)
for j in range(len(combinaciones[n_mejor])):
  print("valor:   ",valores[combinaciones[n_mejor][j]])
  print("volumen: ",volumenes[combinaciones[n_mejor][j]])
  acum_valores = acum_valores + valores[combinaciones[n_mejor][j]]
  acum_volumenes = acum_volumenes + volumenes[combinaciones[n_mejor][j]]

print("valor total:   ", acum_valores)
print("volumen total: ", acum_volumenes)
