
def combinations():
  c = [[]]
  for x in range(4):
      for r in c:
        c= c + [r+[x]]
  return c
combinaciones = combinations()
print(combinaciones)
