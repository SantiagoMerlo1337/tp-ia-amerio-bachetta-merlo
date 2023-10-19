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


def jugar(filas, columnas, pisos, salida, piezas, pieza_sacar):

    class RushHour3DProblem(SearchProblem):
        def actions(self, state): 
            available_actions = []

            #Se realiza la verificiacion de movimientos permitidos dentro de los limites de la grilla
            for pieza in piezas:
                id, piso, partes = pieza

                resultado = any(map(lambda parte: parte[0] == 0, partes))
                if not resultado:
                    available_actions.append((id, "arriba"))
                
                resultado = any(map(lambda parte: parte[filas-1] == filas-1, partes))
                if not resultado:
                    available_actions.append((id, "abajo"))

                resultado = any(map(lambda parte: parte[0] == 0, partes))
                if not resultado:
                    available_actions.append((id, "izquierda"))
                    
                resultado = any(map(lambda parte: parte[columnas-1] == columnas-1, partes))
                if not resultado:
                    available_actions.append((id, "derecha"))

                if piso == 0:
                    available_actions.append((id, "trepar"))
                elif piso == pisos:
                    available_actions.append((id, "caer"))
                else:
                    available_actions.append((id, "trepar"))
                    available_actions.append((id, "caer"))
            
                new_available_actions = [] #creo una lista nueva para no modificar la original ya que la tengo que recorrer

                for actions in available_actions:
                    estado_resultante = self.result(state, actions)
                    for pieza in estado_resultante: #recorro las pieza por pieza del estado resultante
                        id, piso, partes = pieza #descuageringo
                        for parte in partes: #recorro las partes que conforma la pieza en cuestion
                            for pieza2 in estado_resultante: #recorro de nuevo las piezas del estado resultante
                                id2, piso2, partes2 = pieza2 #descuageringo
                                flag = False #hago una bandera para saber evaluar si hay piezas que se superponen
                                for parte2 in partes2: #recorro pieza por pieza del estado resultante de nuevo para corroborar cada coordenada con el resto
                                    if id2 != id and parte == parte2 and piso == piso2: #corroboro que las coordenadas sean iguales (se superponen) y que no estamos hablando de la misma pieza
                                        flag = True
                                        break
                                if flag == False: #si despues de comparar igualdad de coordenadas entre distintas piezas no se activó el flag quiere decir que no se superpone con ninguna
                                    new_available_actions.append(actions)


    
        def result(self, state, action):
                #ej action = ("pieza_verde", "arriba")
                id_pieza_a_mover, accion_a_realizar = action
                lista_piezas_totales = list(state)

                pieza = map(lambda pieza: pieza[0] == id_pieza_a_mover, lista_piezas_totales) #busca la pieza a mover para obtener los datos a cambiar.
                id, piso, partes = pieza

                #Cambia el valor de todas las filas o columnas dependiendo el tipo de movimiento que haga
                if accion_a_realizar == "arriba":
                    for parte_pieza in partes:
                        fila_pieza, _ = parte_pieza
                        fila_pieza -= 1

                elif accion_a_realizar == "abajo":
                    for parte_pieza in partes:
                        fila_pieza, _ = parte_pieza
                        fila_pieza += 1

                elif accion_a_realizar == "izquierda":
                    for parte_pieza in partes:
                        _, columna_pieza = parte_pieza
                        columna_pieza -= 1

                elif accion_a_realizar == "derecha":
                    for parte_pieza in partes:
                        _, columna_pieza = parte_pieza
                        columna_pieza += 1
                
                #Cambia el valor de los pisos

                elif accion_a_realizar == "trepar":
                    piso += 1
                
                else: # "caer"
                    piso -= 1


        
        def cost(self, state, action, state2):
            return 1
        
        def is_goal(self, state):
            pieza = map(lambda pieza_id: pieza_id[0] == pieza_sacar, state)
            id, piso, partes = pieza
            for parte in partes:
                if parte == salida:
                    return True
            return False
            
        
        def heuristic(self, state):
            pass