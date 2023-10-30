from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    greedy,
    astar,)
from simpleai.search.viewers import (BaseViewer, WebViewer)

def distancia(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def control_sin_superposiciones(estado_resultante):
        lista_partes = []
        for pieza in estado_resultante:
            id, piso, partes = pieza
            for parte in partes:
                lista_partes.append((parte, piso)) # Agrego a la lista todas las partes de todas las piezas con su piso correspondiente

        lista_partes_sin_repetidos = set(lista_partes) # Hago un set de lista partes        
        if len(lista_partes_sin_repetidos) == len(lista_partes): # Si son distintos quiere decir que en lista_partes habia elementos repetidos
            return True # La accion es valida: no hay superposicion
        else:
            return False # La accion no es valida: hay superposicion de piezas

class RushHour3DProblem(SearchProblem):
    
    def __init__(self, filas, columnas, pisos, salida, pieza_sacar, initial_state=None):
        self.filas = filas
        self.columnas = columnas
        self.pisos = pisos - 1
        self.salida = salida
        self.pieza_sacar = pieza_sacar

        super().__init__(initial_state)

    def actions(self, state): 
        acciones_disponibles = []
    
        for pieza in state:
            id_pieza_a_mover, piso, partes = pieza
            resultado = any(part[0] == 0 for part in partes) # Si alguna de las partes de la pieza esta en la fila 0 (cero) retorna True
            if not resultado:
                acciones_disponibles.append((id_pieza_a_mover, "arriba"))
            resultado = any(part[0] == self.filas - 1 for part in partes)
            if not resultado:
                acciones_disponibles.append((id_pieza_a_mover, "abajo"))
            resultado = any(part[1] == 0 for part in partes)
            if not resultado:
                acciones_disponibles.append((id_pieza_a_mover, "izquierda"))
            resultado = any(part[1] == self.columnas - 1 for part in partes)
            if not resultado:
                acciones_disponibles.append((id_pieza_a_mover, "derecha"))

            if self.pisos > 0:
                if piso == 0:
                    acciones_disponibles.append((id_pieza_a_mover, "trepar"))
                elif piso == self.pisos:
                    acciones_disponibles.append((id_pieza_a_mover, "caer"))
                else:
                    acciones_disponibles.append((id_pieza_a_mover, "trepar"))
                    acciones_disponibles.append((id_pieza_a_mover, "caer"))

        nuevas_acciones_disponibles = [] # Creo una lista nueva para no modificar la original ya que la tengo que recorrer
        for action in acciones_disponibles:
            estado_resultante = self.result(state, action)
            es_valido = control_sin_superposiciones(estado_resultante)
            if es_valido:
                nuevas_acciones_disponibles.append(action)

        return nuevas_acciones_disponibles


    def result(self, state, action):
            # Ej action = ("pieza_verde", "arriba")
            id_pieza_a_mover, accion_a_realizar = action
            lista_piezas_totales = list(state)

            # Busca la pieza a mover para obtener los datos a cambiar.
            for i, pieza in enumerate(lista_piezas_totales):
                if pieza[0] == id_pieza_a_mover:
                    id, piso, partes = pieza
                    nuevas_partes = []  # Crear una lista para las partes actualizadas de la pieza
                    nuevo_piso = piso

                    # Cambiar el valor de todas las filas o columnas dependiendo del tipo de movimiento que haga
                    for parte_pieza in partes:
                        fila_pieza, columna_pieza = parte_pieza
                        if accion_a_realizar == "arriba":
                            fila_pieza -= 1
                        elif accion_a_realizar == "abajo":
                            fila_pieza += 1
                        elif accion_a_realizar == "izquierda":
                            columna_pieza -= 1
                        elif accion_a_realizar == "derecha":
                            columna_pieza += 1
                        elif accion_a_realizar == "trepar":
                            nuevo_piso = piso + 1
                        else: # "caer"
                            nuevo_piso = piso - 1
                        nuevas_partes.append((fila_pieza, columna_pieza))
                    # Actualizar la pieza en la lista
                    lista_piezas_totales[i] = (id, nuevo_piso, tuple(nuevas_partes))
            return tuple(lista_piezas_totales)


    def cost(self, state, action, state2):
        return 1


    def is_goal(self, state):
        pieza = [pieza for pieza in state if pieza[0] == self.pieza_sacar]
        piso_salida, fila_salida, columna_salida = self.salida
        id, piso, partes = pieza[0]
        for parte in partes:
            if parte == (fila_salida, columna_salida) and piso == piso_salida: # Es goal si alguna de las parte de la pieza_a_sacar esta en la salida y se encuentran en el mismo piso
                return True
        return False
    
    
    def heuristic(self, state):
        costo_total = 0
        piso_salida, fila_salida, columna_salida = self.salida
        pieza = [pieza for pieza in state if pieza[0] == self.pieza_sacar]
        lista_resultados = []
        for parte_pieza in pieza[0][2]: # Recorro todas las partes de la pieza a sacar
            lista_resultados.append((distancia(parte_pieza, (fila_salida, columna_salida)))) # Guardo en una lista los resultados del manhattan con cada parte de la pieza
        costo_total += min(lista_resultados) # Elijo la de menor distancia para no sobreestimar
        costo_total += abs(piso_salida - pieza[0][1]) # Agrego la diferencia entre los pisos de la salida y la pieza_a_sacar
        return costo_total
        

def jugar(filas, columnas, pisos, salida, piezas, pieza_sacar):

    initial_state = tuple([(nombre, piso, tuple(coord)) for (nombre, piso, coord) in (pieza.values() for pieza in piezas)])

    # initial_state = piezas

    my_problem = RushHour3DProblem(filas, columnas, pisos, salida, pieza_sacar, initial_state)

    result = astar(my_problem)
    
    return [ action for action, state in result.path() ][1:]