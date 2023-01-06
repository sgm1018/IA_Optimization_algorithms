#If u dont have this library, install it on terminal with this comand:  :)
#pip install networkx
#pip install matplotlib

#--------------------------------------------LIBRERIAS#--------------------------------------------#

import random    
import networkx as nx
import matplotlib.pyplot as plt
import math
#--------------------------------------------PARAMETROS DE LOS ALGORITMOS#--------------------------------------------#

vertices = 6
nAristas = 7
kValue = 4
listaEnlaces = [(1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 4), (4, 6)]
poblacion_inicial = 10
max_generaciones = 100
tasa_mutacion = 0.1

#--------------------------------------------FUNCIONES ADICIONALES#--------------------------------------------#
def load(dir):
    
    with open(dir, 'r') as f:
        kValue=0
        vertices=0
        nAristas=0
        listaEnlaces=[]
        for line in f:
            words = line.split(' ')
            if (words[0] == 'k'):
                kValue=int(words[1])
            if (words[1]=='edge'):
                vertices=int(words[2])
                nAristas=int(words[3])
            if(words[0]=='e'):
                listaEnlaces.append((int(words[1]),int(words[2])))
            
    return kValue,vertices,nAristas,listaEnlaces            

def showGraph(listaEnlaces):
        # Crea un grafo vacío
    G = nx.Graph()
    # Añade los enlaces a la lista de enlaces del grafo
    G.add_edges_from(listaEnlaces)
    # Dibuja el grafo
    
    # Dibuja el grafo
    
    nx.draw(G,with_labels=True)
    # Muestra el gráfico
    plt.show()

# Función de aptitud
def aptitud(individuo):
    nAristasSubconjunto = 0
    for (a, b) in listaEnlaces:
        if a in individuo and b in individuo:
            nAristasSubconjunto += 1
    return nAristasSubconjunto

# Operador de recombinación por un punto
def recombinacion_punto(ind1, ind2):
    punto = random.randint(1, kValue-1)
    return ind1[:punto] + ind2[punto:]

# Operador de recombinación uniforme
def recombinacion_uniforme(ind1, ind2):
    hijo = []
    for i in range(kValue):
        if random.random() < 0.5:
            hijo.append(ind1[i])
        else:
            hijo.append(ind2[i])
    return hijo

# Operador de mutación por intercambio
def mutacion_intercambio(ind):
    i = random.randint(0, kValue-1)
    j = random.randint(0, kValue-1)
    ind[i], ind[j] = ind[j], ind[i]

# Operador de mutación por inserción
def mutacion_insercion(ind):
    i = random.randint(0, kValue-1)
    j = random.randint(0, kValue-1)
    ind.pop(i)
    ind.insert(j, i)

# Método de selección por torneo
def seleccion_torneo(poblacion):
    ind1 = random.choice(poblacion)
    ind2 = random.choice(poblacion)
    if aptitud(ind1) > aptitud(ind2):
        return ind1
    else:
        return ind2

# Método de selección por ruleta
def seleccion_ruleta(poblacion):
    suma_aptitudes = sum([aptitud(ind) for ind in poblacion])
    probabilidades = [aptitud(ind) / suma_aptitudes for ind in poblacion]
    acumuladas = [probabilidades[0]]
    for p in probabilidades[1:]:
        acumuladas.append(acumuladas[-1] + p)
    r = random.random()
    for (ind, acumulada) in zip(poblacion, acumuladas):
        if r < acumulada:
            return ind
#--------------------------------------------FUNCIONES ADICIONALES#--------------------------------------------#

#--------------------------------------------Main#--------------------------------------------#
def main():
    dir = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\datos.txt'
    #kValue,vertices,nAristas,listaEnlaces = load(dir)
    #showGraph()
    AlgoritmoGreedy()
    evolutiveAlgorithm()
    #algoritmoHibrido()
    
#--------------------------------------------ALGORITMOS#--------------------------------------------#
#Algoritmo Busqueda Local
def AlgoritmoGreedy():

    #vertices = 6
    #nAristas = 7
    #kValue = 4
    #listaEnlaces = [(1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 4), (4, 6)]

    # Crea una lista de tuplas con los vértices y el número de vecinos
    vecinos = []
    for i in range(vertices):
        vecinos.append((i+1, 0))

    for (a, b) in enlaces:
        vecinos[a-1] = (a, vecinos[a-1][1]+1)
        vecinos[b-1] = (b, vecinos[b-1][1]+1)

    # Ordena la lista de tuplas en orden descendente por el número de vecinos
    vecinos.sort(key=lambda x: x[1], reverse=True)

    # Selecciona los k vértices con más vecinos
    subconjunto = []
    for i in range(kValue):
        subconjunto.append(vecinos[i][0])

    # Cuenta el número de aristas entre los vértices seleccionados
    nAristasSubconjunto = 0
    for (a, b) in enlaces:
        if a in subconjunto and b in subconjunto:
            nAristasSubconjunto += 1

    print(sorted(subconjunto, reverse=True),"-> Number of Edges: ",nAristasSubconjunto)
    
#Algoritmo Evolutivo  
def evolutiveAlgorithm():
    # Crea la población inicial
    poblacion = [[random.randint(1, vertices) for _ in range(kValue)] for _ in range(poblacion_inicial)]
    # Crea la población inicial
    poblacion = [[random.randint(1, vertices) for _ in range(kValue)] for _ in range(poblacion_inicial)]

    # Itera hasta el criterio de parada
    for _ in range(max_generaciones):
        # Selecciona a los individuos para reproducirse
        seleccionados_torneo = [seleccion_torneo(poblacion) for _ in range(poblacion_inicial)]
        seleccionados_ruleta = [seleccion_ruleta(poblacion) for _ in range(poblacion_inicial)]
        # Aplica los operadores de recombinación
        hijos_torneo = [recombinacion_punto(seleccionados_torneo[i], seleccionados_torneo[i+1]) for i in range(0, poblacion_inicial, 2)]
        hijos_ruleta = [recombinacion_uniforme(seleccionados_ruleta[i], seleccionados_ruleta[i+1]) for i in range(0, poblacion_inicial, 2)]
        # Aplica los operadores de mutación
        for ind in hijos_torneo:
            if random.random() < tasa_mutacion:
                mutacion_intercambio(ind)
        for ind in hijos_ruleta:
            if random.random() < tasa_mutacion:
                mutacion_insercion(ind)

        # Reemplaza a algunos individuos de la población
        poblacion = hijos_torneo[:int(poblacion_inicial/2)] + hijos_ruleta[:int(poblacion_inicial/2)] + seleccionados_torneo[:int(poblacion_inicial/2)] + seleccionados_ruleta[:int(poblacion_inicial/2)]
        # Obtiene el mejor individuo
    mejor = max(poblacion, key=aptitud)
    print(sorted(mejor,reverse=True),"Number of Edges = ",aptitud(mejor))
    
#Algoritmo Hibrido          
def algoritmoHibrido():
    MAX_GENERACIONES_EVOLUTIVO=10
            # Inicializa el mejor individuo con una solución aleatoria
    mejor = [random.randint(1, vertices) for _ in range(kValue)]
    mejor_aptitud = aptitud(mejor)

    # Itera hasta el criterio de parada
    for _ in range(max_generaciones):
        # Crea la población inicial
        poblacion = [[random.randint(1, vertices) for _ in range(kValue)] for _ in range(poblacion_inicial)]
        # Aplica el algoritmo evolutivo
        for _ in range(MAX_GENERACIONES_EVOLUTIVO):
            # Selecciona a los individuos para reproducirse
            seleccionados_torneo = [seleccion_torneo(poblacion) for _ in range(poblacion_inicial)]
            seleccionados_ruleta = [seleccion_ruleta(poblacion) for _ in range(poblacion_inicial)]
            # Aplica los operadores de recombinación
            hijos_torneo = [recombinacion_punto(seleccionados_torneo[i], seleccionados_torneo[i+1]) for i in range(0, poblacion_inicial, 2)]
            hijos_ruleta = [recombinacion_uniforme(seleccionados_ruleta[i], seleccionados_ruleta[i+1]) for i in range(0, poblacion_inicial, 2)]
            # Aplica los operadores de mutación
            for ind in hijos_torneo:
                if random.random() < tasa_mutacion:
                    mutacion_intercambio(ind)
            for ind in hijos_ruleta:
                if random.random() < tasa_mutacion:
                    mutacion_insercion(ind)
            # Reemplaza a algunos individuos de la población
            poblacion = hijos_torneo[:int(poblacion_inicial/2)] + hijos_ruleta[:int(poblacion_inicial/2)] + seleccionados_torneo[:int(poblacion_inicial/2)] + seleccionados_ruleta[:int(poblacion_inicial/2)]
        # Aplica la búsqueda local sobre el mejor individuo del algoritmo evolutivo
        mejor_evolutivo = max(poblacion, key=aptitud)
        print(mejor_evolutivo)
        mejor_local = AlgoritmoGreedy(mejor_evolutivo)
        mejor_aptitud_local = aptitud(mejor_local)
        # Actualiza el mejor individuo
        if mejor_aptitud_local > mejor_aptitud:
            mejor = mejor_local
            mejor_aptitud = mejor_aptitud_local

    print(mejor, mejor_aptitud)
if __name__ == "__main__":
    main()  
