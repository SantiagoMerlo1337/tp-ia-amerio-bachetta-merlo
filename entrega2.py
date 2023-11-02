from simpleai.search import CspProblem, backtrack, min_conflicts
from itertools import combinations

dominios={}
restricciones = []

FORMAS = {
    "L": [(1,0),(1,1)],

    "T": [(0,1),(0,2),(1,1)],

    "O": [(0,1),(1,0),(1,1)],

    "I": [(1,0),(2,0)],

    "-": [(0,1),(0,2)],

    "Z": [(0,1),(1,1),(1,2)],

    ".": []
    }

def armar_tablero(filas, columnas, pisos, salida, piezas, pieza_sacar): 
    problem_variables = [pieza for pieza in range(len(piezas))]
    for variable in problem_variables:
        for piso in range(pisos):
            for row in range(filas):
                for col in range(columnas):
                    dominios[variable] = [(piso, row, col)]

    def verificar_superposicion_piezas(variables, values):
        pass
        
    
    for variable1, variable2 in combinations(problem_variables, 2):
        restricciones.append(((variable1, variable2), verificar_superposicion_piezas))
    

    #Verifico que la salida no se encuentre en el mismo piso que la pieza a sacar
    def verificar_piso_pieza_sacar(variables, values):
        if values[0][0] == salida[0]:
            return False
        return True
    restricciones.append(((pieza_sacar), verificar_piso_pieza_sacar))


    #Verifico que las piezas no se encuentren en el casillero salida
    def verificar_casillero_salida(variables, values):
        piso, row, col = values[0][0]
        forma = values[1][1]
        lista_partes_pieza = obtener_lista_partes_pieza((piso, row, col), forma)
        if salida in lista_partes_pieza:
            return False
        return True
    for i, pieza in enumerate(problem_variables):
        restricciones.append(((pieza, piezas[i]), verificar_casillero_salida))

    #Verifica que haya piezas en todos los pisos
    def verificar_piezas_piso(variables, values):
        lista_piezas_piso = [coord[0] for coord in values]
        lista_piezas_piso = set(lista_piezas_piso)
        if len(lista_piezas_piso) < pisos:
            return False
        return True
    restricciones.append((problem_variables, verificar_piezas_piso))



    # Obtengo una lista de las partes de las piezas
    def obtener_lista_partes_pieza(coord_dominio, forma_pieza):
        lista_partes_pieza = []
        piso, row, col = coord_dominio
        lista_partes_pieza.append(coord_dominio)
        for x in FORMAS[forma_pieza]:
            row_f, col_f = x
            nueva_coord = (piso, row + row_f, col + col_f)
            lista_partes_pieza.append(nueva_coord)
        return tuple(lista_partes_pieza)


             
    problema = CspProblem(problem_variables, dominios, restricciones)
    solucion = min_conflicts()

if __name__ == "__main__":
        pisos = 2
        filas = 2
        columnas = 2
        pieza_sacar = "pieza_roja"
        salida =  (0, 0, 0)
        piezas = {
                "pieza_verde": ".",
                "pieza_roja": ".",
                }

        problem = CspProblem(piezas, dominios, restricciones)
        solution = min_conflicts(problem)

        print("Solucion:")
        print(solution)