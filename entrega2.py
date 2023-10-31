from simpleai.search import (CspProblem, backtrack, min_conflicts)

dominios={}
restricciones = []
FORMAS = {
     "L": ((1,0),(1,1)),

     "T": ((0,1),(0,2),(1,1)),

     "O": ((0,1),(1,0),(1,1)),

     "I": ((1,0),(2,0)),

     "-": ((0,1),(0,2)),

     "Z": ((0,1),(1,1),(1,2)),

     ".": ()
     }

def armar_mapa(filas, columnas, pisos, salida, piezas, pieza_sacar): 
    problem_variables = [pieza for pieza in range(len(piezas))]
    for variable in problem_variables:
          for piso in enumerate(pisos-1):
               for row in enumerate(filas-1):
                    for col in enumerate(columnas-1):
                         dominios[variable] = [(row, col, piso)]