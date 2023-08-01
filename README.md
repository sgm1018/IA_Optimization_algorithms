## Optimization Algorithms - University of COIMBRA ISEC - Erasmus Period

This README provides an overview of the optimization algorithms implemented for solving the optimization problem. The algorithms are applied to a graph represented by a set of vertices and edges.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Algorithms](#algorithms)
    - [Greedy Algorithm](#greedy-algorithm)
    - [Stochastic Hill Climbing](#stochastic-hill-climbing)
    - [Evolutionary Algorithm](#evolutionary-algorithm)
    - [Hybrid Algorithms](#hybrid-algorithms)
- [Examples](#examples)
- [Author](#author)

## Introduction

This project was developed during the Erasmus period at the University of COIMBRA ISEC. It focuses on solving the optimization problem of finding a subgraph with a maximum number of edges under certain constraints.

## Requirements

To run the algorithms, you need to have the following libraries installed:

- [networkx](https://networkx.org/)
- [matplotlib](https://matplotlib.org/)

You can install these libraries using pip:

```bash
pip install networkx
pip install matplotlib
```

## Getting Started

Clone the repository to your local machine and navigate to the project directory.
```bash
git clone <repository_url>
cd optimization-algorithms
```

## Usage
To use the optimization algorithms, import the required functions from the optimization module.
```python
from optimization import AlgoritmoGreedy, hill_climbingEstocastico, evolutiveAlgorithm, algoritmo_Hibrido_Greedy_Evolutivo, algoritmo_Hibrido_Estocastico_Evolutivo, algoritmo_Hibrido_Estocastico_Evolutivo2
```
## Algorithms
### Greedy Algorithm
The Greedy algorithm aims to find a subgraph by selecting the vertices with the highest number of neighbors. It iteratively selects the vertices with the highest degree until a stopping criterion is met.
```python
AlgoritmoGreedy(maxIterations=1500, max_iteraciones_SinMejora=1000)
```

## Stochastic Hill Climbing
Stochastic Hill Climbing is a local search algorithm that starts with a random initial solution and iteratively improves it by making small random changes to the current solution. It stops when no better solution can be found in the neighborhood.
```python
evolutiveAlgorithm(poblacion_inicial=10, max_generaciones=100, tasa_mutacion=0.1)
```
## Hybrid Algorithms
There are two hybrid algorithms implemented, combining the Greedy algorithm with the Evolutionary algorithm and Stochastic Hill Climbing respectively.
```python
algoritmo_Hibrido_Greedy_Evolutivo(poblacion_inicial=10, max_generaciones=100, tasa_mutacion=0.1)
algoritmo_Hibrido_Estocastico_Evolutivo(poblacion_inicial=10, max_generaciones=100, max_iterations=1000)
algoritmo_Hibrido_Estocastico_Evolutivo2(poblacion_inicial=10, max_generaciones=100, max_iterations=1000)
```

## Examples
The following examples demonstrate the usage of the algorithms with different input files:

# Example with dirTest file
```python
kValue, vertices, nAristas, listaEnlaces = load(dirTest)
print("------------Test File------------")
print("Greedy Algorithm:")
AlgoritmoGreedy()
print("Stochastic Hill Climbing:")
print(hill_climbingEstocastico())
print("Evolutionary Algorithm:")
evolutiveAlgorithm()
print("Hybrid Algorithm (Greedy + Evolutionary):")
algoritmo_Hibrido_Greedy_Evolutivo()
print("Hybrid Algorithm (Stochastic Hill Climbing + Evolutionary):")
algoritmo_Hibrido_Estocastico_Evolutivo()
print("Hybrid Algorithm (Stochastic Hill Climbing + Evolutionary 2):")
algoritmo_Hibrido_Estocastico_Evolutivo2()
```

## Author
These algorithms have been made by **sgm1018**



