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

class RushHour3DProblem(SearchProblem):
    
    def __init__(self, filas, columnas, pisos, salida, pieza_sacar, initial_state=None):
        self.filas = filas
        self.columnas = columnas
        self.pisos = pisos
        self.salida = salida
        self.pieza_sacar = pieza_sacar

        super().__init__(initial_state)


    def actions(self, state): 
        available_actions = []
    
        for pieza in state:
            id_pieza_a_mover, piso, partes = pieza

            resultado = any(part[0] == 0 for part in partes)
            if not resultado:
                available_actions.append((id_pieza_a_mover, "arriba"))

            resultado = any(part[0] == self.filas - 1 for part in partes)
            if not resultado:
                available_actions.append((id_pieza_a_mover, "abajo"))

            resultado = any(part[1] == 0 for part in partes)
            if not resultado:
                available_actions.append((id_pieza_a_mover, "izquierda"))

            resultado = any(part[1] == self.columnas - 1 for part in partes)
            if not resultado:
                available_actions.append((id_pieza_a_mover, "derecha"))

            if self.pisos > 1:
                if piso == 1:
                    available_actions.append((id_pieza_a_mover, "trepar"))
                elif piso == self.pisos:
                    available_actions.append((id_pieza_a_mover, "caer"))
                else:
                    available_actions.append((id_pieza_a_mover, "trepar"))
                    available_actions.append((id_pieza_a_mover, "caer"))

        new_available_actions = [] # Creo una lista nueva para no modificar la original ya que la tengo que recorrer

        for action in available_actions:
            estado_resultante = self.result(list(state), action)

            for pieza in estado_resultante: # Recorro las pieza por pieza del estado resultante
                id2, piso2, partes2 = pieza # Desestructuro
                flag = False # Hago una bandera para saber si hay piezas que se superponen

                for parte in partes:
                    for parte2 in partes2: # Recorro pieza por pieza del estado resultante de nuevo para corroborar cada coordenada con el resto
                        if id2 != id_pieza_a_mover and parte == parte2 and piso == piso2: # Corroboro que las coordenadas sean iguales (se superponen) y que no estamos hablando de la misma pieza
                            flag = True
                            break

                if not flag: # Si después de comparar igualdad de coordenadas entre distintas piezas no se activó la bandera, significa que no se superponen con ninguna
                    new_available_actions.append(action)

        return new_available_actions



    def result(self, state, action):
            # #ej action = ("pieza_verde", "arriba")
            
            id_pieza_a_mover, accion_a_realizar = action
            lista_piezas_totales = list(state)

            # busca la pieza a mover para obtener los datos a cambiar.
            for i, pieza in enumerate(lista_piezas_totales):
                if pieza[0] == id_pieza_a_mover:
                    id, piso, partes = pieza
                    nuevas_partes = []  # crear una lista para las partes actualizadas de la pieza
                    nuevo_piso = piso
                    # cambiar el valor de todas las filas o columnas dependiendo del tipo de movimiento que haga
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

                    # actualizar la pieza en la lista
                    lista_piezas_totales[i] = (id, nuevo_piso, tuple(nuevas_partes))

            return tuple(lista_piezas_totales)

            

    def cost(self, state, action, state2):
        return 1


    def is_goal(self, state):
        pieza = [pieza for pieza in state if pieza[0] == self.pieza_sacar]

        piso_salida, fila_salida, columna_salida = self.salida
        
        id, piso, partes = pieza[0]
        
        for parte in partes:
            if parte == (fila_salida, columna_salida) and piso == piso_salida:
                return True
        return False
    
    def heuristic(self, state):
        costo_total = 0
        piso_salida, fila_salida, columna_salida = self.salida
        pieza = [pieza for pieza in state if pieza[0] == self.pieza_sacar]
        lista_resultados = []
        for parte_pieza in pieza[0][2]:
            lista_resultados.append((distancia(parte_pieza, (fila_salida, columna_salida))))
        costo_total += min(lista_resultados)
        costo_total += abs(piso_salida - pieza[0][1])
        return costo_total

            
        

def jugar(filas, columnas, pisos, salida, piezas, pieza_sacar):

    initial_state = tuple([(nombre, piso, tuple(coord)) for (nombre, piso, coord) in (pieza.values() for pieza in piezas)])

    # initial_state = piezas

    my_problem = RushHour3DProblem(filas, columnas, pisos, salida, pieza_sacar, initial_state)

    result = astar(my_problem)
    
    return [ action for action, state in result.path() ][1:]

    # if result is None:
    #     print("No solution")
    # else:
    #     for action, state in result.path():
    #         print("A:", action)
    #         print("S:")
    #         print(*state, sep="\n")

    #     print("Final depth:", len(result.path()))
    #     print("Final cost:", result.cost)
    # print("Stats:")


if __name__ == "__main__":
    print(jugar(
        filas = 3,
        columnas= 3,
        pisos= 1,
        salida=(1, 2, 2),
        piezas=[{"id": "pieza_verde", "piso": 1, "partes": [(0,0), (0,1)]}],
        pieza_sacar="pieza_verde",
    ))