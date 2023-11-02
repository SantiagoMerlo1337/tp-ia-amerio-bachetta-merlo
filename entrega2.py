from simpleai.search import CspProblem, backtrack, min_conflicts
from itertools import combinations

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
    restricciones = []
    DICCIONARIO_PIEZAS = dict(piezas)
    problem_variables = [pieza[0] for pieza in piezas]
    dominios = {}
    for variable in problem_variables:
        dominio = []
        forma = FORMAS[DICCIONARIO_PIEZAS[variable]]
        for piso in range(pisos):
            for row in range(filas - (max([row[0] for row in forma]) if forma != [] else 0)):
                for col in range(columnas - (max([col[1] for col in forma ]) if forma != [] else 0)):
                    dominio.append((piso, row, col))
        dominios[variable] = dominio


    # Obtengo una lista de las partes de las piezas
    def obtener_lista_partes_pieza(coord_dominio, forma_pieza):
        lista_partes_pieza = []
        piso, row, col = coord_dominio
        lista_partes_pieza.append(coord_dominio)
        for x in FORMAS[forma_pieza]:
            row_f, col_f = x
            nueva_coord = (piso, row + row_f, col + col_f)
            lista_partes_pieza.append(nueva_coord)
        return lista_partes_pieza


    def verificar_superposicion_piezas(variables, values):
        # print("verificar_superposicion_piezas")
        forma_pieza1 = DICCIONARIO_PIEZAS[variables[0]]
        forma_pieza2 = DICCIONARIO_PIEZAS[variables[1]]
        coord_pieza1 = values[0]
        coord_pieza2 = values[1]
        lista_partes_pieza1 = obtener_lista_partes_pieza(coord_pieza1, forma_pieza1)
        lista_partes_pieza2 = obtener_lista_partes_pieza(coord_pieza2, forma_pieza2)
        lista_partes_totales = lista_partes_pieza1 + lista_partes_pieza2
        if len(lista_partes_totales) > len(set(lista_partes_totales)):
            return False
        return True

    for variable1, variable2 in combinations(problem_variables, 2):
        restricciones.append(((variable1, variable2), verificar_superposicion_piezas))


    #Verifico que la salida no se encuentre en el mismo piso que la pieza a sacar
    def verificar_piso_pieza_sacar(variables, values):
        if values[0][0] == salida[0]:
            return False
        return True

    restricciones.append(([pieza_sacar], verificar_piso_pieza_sacar))


    #Verifico que las piezas no se encuentren en el casillero salida
    def verificar_casillero_salida(variables, values):
        # print("verificar_casillero_salida")
        piso, row, col = values[0]
        forma = DICCIONARIO_PIEZAS[variables[0]]
        lista_partes_pieza = obtener_lista_partes_pieza((piso, row, col), forma)
        if salida in lista_partes_pieza:
            return False
        return True
    
    for variable in problem_variables:
        restricciones.append(([variable], verificar_casillero_salida))


    #Verifica que haya piezas en todos los pisos
    def verificar_piezas_piso(variables, values):
        # print("verificar_piezas_piso")
        lista_piezas_piso = [coord[0] for coord in values]
        lista_piezas_piso = set(lista_piezas_piso)
        if len(lista_piezas_piso) < pisos:
            return False
        return True
    
    restricciones.append((problem_variables, verificar_piezas_piso))


    #Verificar que ningun piso tiene mas del doble de piezas que ningun otro
    def verificar_piezas_dobles_piso(variables, values):
        # print("verificar_piezas_dobles_piso")
        conteo = {}
        for coord in values:
            piso,_,_ = coord
            if piso in conteo:
                conteo[piso] += 1
            else:
                conteo[piso] = 1

        piso_menos_repetido = min(conteo.values())

        for coord in values:
            piso,_,_ = coord
            if conteo[piso] > piso_menos_repetido * 2:
                return False
        return True
        
    restricciones.append((problem_variables, verificar_piezas_dobles_piso))


    #Cantidad de casilleros que ocupan 
    def verificar_cantidad_partes_piezas_en_casilleros(variables, values):
        for piso in range(pisos):
            count_piso = 0
            for i, coord in enumerate(values):
                piso_coord, _, _ = coord
                if piso == piso_coord:
                    print(FORMAS[DICCIONARIO_PIEZAS[variables[i]]])
                    count_piso += len(FORMAS[DICCIONARIO_PIEZAS[variables[i]]]) + 1
            print(count_piso)
            if count_piso > filas * columnas * (2/3):
                return False
        return True

    restricciones.append((problem_variables, verificar_cantidad_partes_piezas_en_casilleros))


    problema = CspProblem(problem_variables, dominios, restricciones)
    solucion = min_conflicts(problema)
    return solucion