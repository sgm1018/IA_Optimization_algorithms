#If u dont have this library, install it on terminal with this comand:  :)
#pip install networkx
#pip install matplotlib

#--------------------------------------------LIBRERIAS#--------------------------------------------#

import random    
import networkx as nx
import matplotlib.pyplot as plt
import math

#--------------------------------------------LeerTxt#----------------------------------------------#
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
#--------------------------------------------PARAMETROS DE LOS ALGORITMOS#--------------------------------------------#


#--------------------------------------------FUNCIONES ADICIONALES#--------------------------------------------#
           

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
def reproduccion(padres):
    # Aplicamos el cruce en el punto medio para crear dos descendientes
    descendiente1 = padres[0][:len(padres[0]) // 2] + padres[1][len(padres[1]) // 2:]
    descendiente2 = padres[1][:len(padres[1]) // 2] + padres[0][len(padres[0]) // 2:]
    return [descendiente1, descendiente2]

def mutacion(individuo):
    # Cambiamos el valor de un gen al azar
    gen = random.randint(0, len(individuo) - 1)
    individuo[gen] = random.randint(1, vertices)
    return individuo
#--------------------------------------------FUNCIONES ADICIONALES#--------------------------------------------#


#Algoritmo Busqueda Local
def AlgoritmoGreedy(maxIterations=1500,max_iteraciones_SinMejora=1000):
    iterations = 0 
    # Crea una lista de tuplas con los vértices y el número de vecinos
    vecinos = []
    for i in range(vertices):
        vecinos.append((i+1, 0))

    for (a, b) in listaEnlaces:
        vecinos[a-1] = (a, vecinos[a-1][1]+1)
        vecinos[b-1] = (b, vecinos[b-1][1]+1)

    # Ordena la lista de tuplas en orden descendente por el número de vecinos
    vecinos.sort(key=lambda x: x[1], reverse=True)

    # Inicializa la mejor solución encontrada hasta ahora
    mejor_subconjunto = []
    mejor_nAristasSubconjunto = 0
    
    # Repite el algoritmo varias veces hasta que no se encuentre una solución mejor durante un cierto número de iteraciones
    n_iteraciones_sin_mejora = 0
    while n_iteraciones_sin_mejora < max_iteraciones_SinMejora:
        iterations +=1
        #Condicion de salida:
        if maxIterations < iterations:
            break
        # Selecciona los k vértices con más vecinos
        subconjunto = []
        for i in range(kValue):
            subconjunto.append(vecinos[i][0])

        # Cuenta el número de aristas entre los vértices seleccionados
        nAristasSubconjunto = 0
        for (a, b) in listaEnlaces:
            if a in subconjunto and b in subconjunto:
                nAristasSubconjunto += 1

        # Si se ha encontrado una solución mejor, actualiza la mejor solución encontrada hasta ahora
        if nAristasSubconjunto > mejor_nAristasSubconjunto:
            mejor_subconjunto = subconjunto
            mejor_nAristasSubconjunto = nAristasSubconjunto
            n_iteraciones_sin_mejora = 0
        else:
            n_iteraciones_sin_mejora += 1

    print(sorted(mejor_subconjunto, reverse=True),"-> n: ",mejor_nAristasSubconjunto)

#Algoritmo Evolutivo  
def evolutiveAlgorithm(poblacion_inicial=10,max_generaciones=100,tasa_mutacion=0.1 ):
    
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
    print(sorted(mejor,reverse=True),"-> Number of Edges = ",aptitud(mejor))
    
def hill_climbingEstocastico(max_iterations=1000):
    iterations=0
# Crea una solución inicial al elegir al azar k vértices del grafo
    solucion_incial = random.sample(range(vertices), kValue)
  
    # Bucle hasta que no se pueda mejorar la solución actual, cada vez que se ejecuta este bucle, busca en un vecindario distinto.
    while True:
    # Crea una lista de posibles cambios a la solución actual
        iterations+=1
        possible_changes = []
        if(iterations>= max_iterations):
            break
    
        # Recorre cada vértice en la solución actual
        for vertex in solucion_incial:
            # Crea una lista de vértices vecinos del vértice actual
            neighbors = [v for (u, v) in listaEnlaces if u == vertex or v == vertex]
        
        # Recorre cada vecino
            for neighbor in neighbors:
                # Si el vecino no está en la solución actual y al menos dos vecinos diferentes han sido explorados,
                # agrega el vecino como un posible cambio a la solución actual
                if neighbor not in solucion_incial and len(set(solucion_incial).intersection(set(neighbors))) > 1:
                    possible_changes.append(neighbor)
        
        # Si no hay posibles cambios, termina el bucle
        if not possible_changes:
            break
        
        # Elige al azar un posible cambio
        change = random.choice(possible_changes)
        
        # Crea una nueva solución reemplazando un vértice al azar en la solución actual con el cambio elegido
        new_solution = solucion_incial[:]
        new_solution.remove(random.choice(solucion_incial))
        new_solution.append(change)
        
        # Calcula el número de aristas en la nueva solución
        new_edges = sum([1 for (u, v) in listaEnlaces if u in new_solution and v in new_solution])
        
        # Si la nueva solución tiene más aristas que la solución actual, la solución actual se convierte en la nueva solución
        if new_edges > sum([1 for (u, v) in listaEnlaces if u in solucion_incial and v in solucion_incial]):
            solucion_incial = new_solution

    # Devuelve la solución final  
    return solucion_incial  
    #print(sorted(current_solution, reverse=True),"-> Number of Edges: ",aptitud(current_solution))
#Algoritmo Hibrido: EVOLUTIVO + GREEDY        

def algoritmo_Hibrido_Greedy_Evolutivo(poblacion_inicial = 10 ,max_generaciones = 100, tasa_mutacion = 0.1 ):
    mejorFinal=[]
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

        # Aplica el algoritmo de búsqueda local greedy a cada individuo en la población
        for i, individuo in enumerate(poblacion):
            vecinos = []
            for i in range(vertices):
                vecinos.append((i+1, 0))

            for (a, b) in listaEnlaces:
                vecinos[a-1] = (a, vecinos[a-1][1]+1)
                vecinos[b-1] = (b, vecinos[b-1][1]+1)

            # Ordena la lista de tuplas en orden descendente por el número de vecinos
            vecinos.sort(key=lambda x: x[1], reverse=True)

            # Selecciona los k vértices con más vecinos
            subconjunto = []
            for i in range(kValue):
                subconjunto.append(vecinos[i][0])
            # Reemplaza al individuo en la población con la solución mejorada obtenida del algoritmo de búsqueda local greedy
            poblacion[i] = subconjunto
        # Obtiene el mejor individuo
        mejor = max(poblacion, key=aptitud)
        #print(aptitud(mejor))
    #Comprobamos las aptitudes para ver cual es la mejor solucion
    if(aptitud(mejor) > aptitud(mejorFinal) ):
        mejorFinal=mejor
    print(sorted(mejorFinal,reverse=True),"-> Number of Edges = ",aptitud(mejorFinal))
    
    
def algoritmo_Hibrido_Estocastico_Evolutivo(poblacion_inicial = 10 ,max_generaciones = 100, max_iterations = 1000): 
    solucionColinas = hill_climbingEstocastico(max_iterations)
    
    # Iteramos hasta el criterio de parada
    for _ in range(max_generaciones):
        # Seleccionamos a los individuos para reproducirse
        seleccionados_torneo = [seleccion_torneo([solucionColinas]) for _ in range(poblacion_inicial)]
        seleccionados_ruleta = [seleccion_ruleta([solucionColinas]) for _ in range(poblacion_inicial)]
        # Aplicamos los operadores de reproducción y mutación
        offspring = reproduccion(seleccionados_torneo) + reproduccion(seleccionados_ruleta)
        offspring = [mutacion(individuo) for individuo in offspring]
        # Evaluamos la aptitud de los individuos
        poblacion = [individuo for individuo in offspring if aptitud(individuo) > aptitud(solucionColinas)] + [solucionColinas]
        # Actualizamos la solución actual con el individuo más apto
        solucionColinas = seleccion_torneo(poblacion)
        
    # Devolvemos la solución final
    print(sorted(solucionColinas,reverse=True),"-> Number of Edges = ",aptitud(solucionColinas))
    
def algoritmo_Hibrido_Estocastico_Evolutivo2(poblacion_inicial = 10 ,max_generaciones = 100, max_iterations =1000):
    # Generamos una solución inicial utilizando el algoritmo de trepa colinas estocástico
    solucionColinas = hill_climbingEstocastico(max_iterations)
    
    # Iteramos hasta el criterio de parada
    for _ in range(max_generaciones):
        # Generamos una población de soluciones vecinas a la solución actual
        poblacion = []
        for _ in range(poblacion_inicial):
            # Creamos una solución vecina intercambiando dos genes al azar
            vecina = solucionColinas[:]
            gen1 = random.randint(0, len(vecina) - 1)
            gen2 = random.randint(0, len(vecina) - 1)
            vecina[gen1], vecina[gen2] = vecina[gen2], vecina[gen1]
            poblacion.append(vecina)
        # Añadimos la solución actual a la población
        poblacion.append(solucionColinas)
        # Seleccionamos al individuo más apto de la población
        solucionColinas = seleccion_torneo(poblacion)
        
    # Devolvemos la solución final
    print(sorted(solucionColinas,reverse=True),"-> Number of Edges = ",aptitud(solucionColinas))   
#--------------------------------------------Main#--------------------------------------------#
dirTest = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\teste.txt'
dirFile1 = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\file1.txt'
dirFile2 = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\file2.txt'
dirFile3 = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\file3.txt'
dirFile4 = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\file4.txt'
dirFile5 = r'C:\Users\Sergi\Desktop\code\Universidad\Erasmus\IA\p2\Entregable\file5.txt'

kValue,vertices,nAristas,listaEnlaces = load(dirTest)
print("------------------------------------TESTE.txt------------------------------------------------")
print("*******************         ALGORITMO LOCAL GREEDY                        *******************")
AlgoritmoGreedy()
print("*******************         ALGORITMO LOCAL ESTOCASTICO                   *******************")
print(sorted(hill_climbingEstocastico(),reverse=True),"-> Number of Edges = ",aptitud(hill_climbingEstocastico()))
print("*******************         ALGORITMO Evolutivo                           *******************")
evolutiveAlgorithm()
print("*******************         ALGORITMO Hibrido GREEDY - EVOLUTIVO          *******************")
algoritmo_Hibrido_Greedy_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO     *******************")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO 2   *******************")
algoritmo_Hibrido_Estocastico_Evolutivo2()
print("")
kValue,vertices,nAristas,listaEnlaces = load(dirFile1)
print("------------------------------------File1.txt------------------------------------------------")
print("*******************         ALGORITMO LOCAL GREEDY                        *******************")
AlgoritmoGreedy()
print("*******************         ALGORITMO LOCAL ESTOCASTICO                   *******************")
print(sorted(hill_climbingEstocastico(),reverse=True),"-> Number of Edges = ",aptitud(hill_climbingEstocastico()))
print("*******************         ALGORITMO Evolutivo                           *******************")
evolutiveAlgorithm()
print("*******************         ALGORITMO Hibrido GREEDY - EVOLUTIVO          *******************")
algoritmo_Hibrido_Greedy_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO     *******************")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO 2   *******************")
algoritmo_Hibrido_Estocastico_Evolutivo2()
print("")
kValue,vertices,nAristas,listaEnlaces = load(dirFile2)
print("------------------------------------File2.txt------------------------------------------------")
print("*******************         ALGORITMO LOCAL GREEDY                        *******************")
AlgoritmoGreedy()
print("*******************         ALGORITMO LOCAL ESTOCASTICO                   *******************")
print(sorted(hill_climbingEstocastico(),reverse=True),"-> Number of Edges = ",aptitud(hill_climbingEstocastico()))
print("*******************         ALGORITMO Evolutivo                           *******************")
evolutiveAlgorithm()
print("*******************         ALGORITMO Hibrido GREEDY - EVOLUTIVO          *******************")
algoritmo_Hibrido_Greedy_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO     *******************")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO 2   *******************")
algoritmo_Hibrido_Estocastico_Evolutivo2()
print("")
kValue,vertices,nAristas,listaEnlaces = load(dirFile3)
print("------------------------------------File3.txt------------------------------------------------")
print("*******************         ALGORITMO LOCAL GREEDY                        *******************")
AlgoritmoGreedy()
print("*******************         ALGORITMO LOCAL ESTOCASTICO                   *******************")
print(sorted(hill_climbingEstocastico(),reverse=True),"-> Number of Edges = ",aptitud(hill_climbingEstocastico()))
print("*******************         ALGORITMO Evolutivo                           *******************")
evolutiveAlgorithm()
print("*******************         ALGORITMO Hibrido GREEDY - EVOLUTIVO          *******************")
algoritmo_Hibrido_Greedy_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO     *******************")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO 2   *******************")
algoritmo_Hibrido_Estocastico_Evolutivo2()
print("")
kValue,vertices,nAristas,listaEnlaces = load(dirFile4)
print("------------------------------------File4.txt------------------------------------------------")
print("*******************         ALGORITMO LOCAL GREEDY                        *******************")
AlgoritmoGreedy()
print("*******************         ALGORITMO LOCAL ESTOCASTICO                   *******************")
print(sorted(hill_climbingEstocastico(),reverse=True),"-> Number of Edges = ",aptitud(hill_climbingEstocastico()))
print("*******************         ALGORITMO Evolutivo                           *******************")
evolutiveAlgorithm()
print("*******************         ALGORITMO Hibrido GREEDY - EVOLUTIVO          *******************")
algoritmo_Hibrido_Greedy_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO     *******************")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO 2   *******************")
algoritmo_Hibrido_Estocastico_Evolutivo2()
print("")
kValue,vertices,nAristas,listaEnlaces = load(dirFile5)
print("------------------------------------File5.txt------------------------------------------------")
print("*******************         ALGORITMO LOCAL GREEDY                        *******************")
AlgoritmoGreedy()
print("*******************         ALGORITMO LOCAL ESTOCASTICO                   *******************")
print(sorted(hill_climbingEstocastico(),reverse=True),"-> Number of Edges = ",aptitud(hill_climbingEstocastico()))
print("*******************         ALGORITMO Evolutivo                           *******************")
evolutiveAlgorithm()
print("*******************         ALGORITMO Hibrido GREEDY - EVOLUTIVO          *******************")
algoritmo_Hibrido_Greedy_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO     *******************")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("*******************         ALGORITMO Hibrido ESTOCASTICO - EVOLUTIVO 2   *******************")
algoritmo_Hibrido_Estocastico_Evolutivo2()
print("") 