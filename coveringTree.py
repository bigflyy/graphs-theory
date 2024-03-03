import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt 
import json
from datetime import datetime
from collections import defaultdict
import math
import sys

#### My files
from Graph import Graph as G
from CONSTS import *

# вершина = vertex / vertices
# дуга = edge / edges



#weird visualisation i might need
# Defining a Class 
class GraphVisualization: 
   
    def __init__(self): 
          
        # visual is a list which stores all  
        # the set of edges that constitutes a 
        # graph 
        self.visual = [] 
          
    # addEdge function inputs the vertices of an 
    # edge and appends it to the visual list 
    def addEdge(self, a, b, weight, color): 
        temp = [a, b, weight, color] 
        self.visual.append(temp) 
          
    # In visualize function GV is an object of 
    # class Graph given by networkx GV.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(GV) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        GV = nx.Graph() 

        for edge in self.visual:
          GV.add_edge(edge[0], edge[1], weight=edge[2], color=edge[3])

        # u - first v - second, d - data ??
        blue = [(u, v) for (u, v, d) in GV.edges(data=True) if d["color"] == "г"]
        orange = [(u, v) for (u, v, d) in GV.edges(data=True) if d["color"] == "о"]

        pos = nx.spring_layout(GV, seed=7)  # positions for all nodes - seed for reproducibility
        # nodes
        nx.draw_networkx_nodes(GV, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(GV, pos, edgelist=blue, width=6, edge_color="b")
        nx.draw_networkx_edges(
        GV, pos, edgelist=orange, width=6, edge_color="r")

        # node labels
        nx.draw_networkx_labels(GV, pos, font_size=20, font_family="sans-serif")
        # edge weight labels
        edge_labels = nx.get_edge_attributes(GV, "weight")
        nx.draw_networkx_edge_labels(GV, pos, edge_labels)



        ax = plt.gca()
        ax.margins(0.08)
        plt.vertex("off")
        plt.tight_layout()
        plt.show()



# Some variables for everything
GV = GraphVisualization() 
edges=[]            # [[vertexOne, vertexTwo, Weight, color], ...]
edges_colored=[]
vertexAmount=0
amountOfedges = 0
adjacencyMatrix = []
vertices_ = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'f', 'g', 'h', 'k', 's', 'm', 'n', 't']
edges_ = [['b', 'a', 529], ['a', 's', 1], ['c', 'a', 3]]

G.createLetterToIndexDict(vertices_)
G.createIndexToLetter(vertices_)

#printMatrix(edgesToAdjMatrix(vertices_, edges_))
#printMatrixDict(edgesToAdjMatrixDict(vertices_, edges_))
G.exportEdges(edges_)
G.exportVertices(vertices_)
adjMatrixDict = G.edgesToAdjMatrixDict(vertices_, edges_)
adjMatrix = G.edgesToAdjMatrix(vertices_, edges_)
G.printMatrixToFile(adjMatrix)
G.printMatrixDictToFile(adjMatrixDict)
vertices__ = []
edges__ = []

# USER INPUT
inputType = int(input(f"Выберите тип ввода:\n "
             f"{MANUAL_INPUT_TYPE}. Ребра типа a b 10.\n "
             f"{MATRIX_INPUT_TYPE}. Ребра по матрице смежности (неориетированный).\n"
             f"{ORIENTED_MATRIX_INPUT_TYPE}. Ребра по матрице смежности (ориентированный).\n"))
if inputType == MANUAL_INPUT_TYPE:
## vertex amount
  vertexAmount = int(input("Введите кол-во вершин: "))
  print(edges)
  ## actually inputing edges 
  print("Вводите ребра в формате a b 10 (первая вершина, вторая, вес). Введите exit чтобы закончить")
  userInput = ""
  while (True):
    userInput = input().split()
    if (userInput == ["exit"]): break
    userInput[2] = int(userInput[2])
    edges.append(userInput)
elif inputType == MATRIX_INPUT_TYPE:
  vertices = input("Введите все вершины через пробел: a b c d ...").split()
  vertexAmount = len(vertices)
  vertexIndex = 0
  for vertexOne in vertices:
    verticesTwoAndWeight = input(f"Введите вершины (кроме {vertices[:vertexIndex]})которым {vertexOne} смежна: ").split()
    vertexIndex+=1
    if verticesTwoAndWeight == '': continue
    for i in range(0,len(verticesTwoAndWeight), 2):
      vertexTwo = verticesTwoAndWeight[i] 
      weight_ = int(verticesTwoAndWeight[i+1])
      edges.append([vertexOne,vertexTwo,weight_])
elif inputType == ORIENTED_MATRIX_INPUT_TYPE:
    vertices = input("Введите все вершины через пробел: a b c d ...").split()
    vertexAmount = len(vertices)
    vertexIndex = 0
    for vertexOne in vertices:
      verticesTwoAndWeight = input(f"Введите вершины которым {vertexOne} смежна: (b 40 c 50 d 20) ").split()
      vertexIndex+=1
      if verticesTwoAndWeight == '': continue
      for i in range(0,len(verticesTwoAndWeight), 2):
        vertexTwo = verticesTwoAndWeight[i] 
        weight_ = int(verticesTwoAndWeight[i+1])
        edges.append([vertexOne,vertexTwo,weight_])
elif inputType == IMPORT_TXT_INPUT_TYPE:
  G.importAdjMatrix(adjMatrix)
# FORMATTING DATA BEFORE DOING ANYTHING AS IT IS EXPECTED TO BE
edges_colored=edges
edges = G.sortEdges(edges)
vertices = sorted(vertices)
# Deleting duplicates
vertices = list(set(vertices)) 

G.createIndexToLetter(vertices)
G.createLetterToIndexDict(vertices)
adjMatrix = G.edgesToAdjMatrix(vertices, edges)



## Main loop to build several graphs on one set of edges
while (True):
  ## graph type
  action = int(input(f"Выберите действие:\n "
                    f"{OUTPUT_MATRIX}. Вывести матрицу смежности."
                    f"{MINIMAL_COVERING_TREE}.Минимальное покрывающее дерево."
                    f"\n{MAXIMUM_COVERING_TREE}.Максимальное покрывающее дерево.\n"
                    f"{FORD_SHORTEST_PATH}. Дерево кратчайших путей по Форду.\n"))
  # SORTING INDICES BY edges WEIGHT
  index = 0
  edges_weights = [x[2] for x in edges]
  print(edges_weights)
  sorted_indices = []
  if action == MINIMAL_COVERING_TREE  or action == MAXIMUM_COVERING_TREE:
    if action==MINIMAL_COVERING_TREE:
      sorted_indices = np.argsort(edges_weights)
    elif action==MAXIMUM_COVERING_TREE:
      sorted_indices = np.argsort(edges_weights)[::-1]

    print("sorted indices : ", sorted_indices)

    output = []
    buketi = []
    curOutputLine=[]
    weight = 0
    # MAIN LOOP BUILDING GRAPH
    
    for i in sorted_indices:
      if len(curOutputLine) > 0:
        if len(curOutputLine[3]) == vertexAmount:
          break
      vertexOne = edges[i][0]
      vertexTwo = edges[i][1]
      if vertexOne == vertexTwo: 
        continue ## This shouldn't be a loop 
      vertexOne, vertexTwo = sortvertex(vertexOne, vertexTwo)
      buketvertexOne = -1
      buketvertexTwo = -1
      ## 0,                            1,   2,   3, 4
      ## [вершина, вершина] - ребро, цвет, вес, б1, б2 ... 
      curOutputLine = [[vertexOne, vertexTwo], "г", edges[i][2]]
      for buket_i in range(len(buketi)):
        if (vertexOne in buketi[buket_i]): buketvertexOne = buket_i
        if (vertexTwo in buketi[buket_i]): buketvertexTwo = buket_i
      ## from same buket
      if buketvertexOne == buketvertexTwo and buketvertexOne != -1:
        curOutputLine[1] = "о"
      ## none are from buket
      elif buketvertexOne == -1 and buketvertexTwo == -1:
        curOutputLine[1]="г"
        buketi.append([vertexOne, vertexTwo]) # new buket created
      ## vertexOne in buket and vertexTwo is not
      elif buketvertexOne == -1 and buketvertexTwo != -1:
        buketi[buketvertexTwo].append(vertexOne)
      ## vertexTwo in buket and vertexOne is not
      elif buketvertexTwo == -1 and buketvertexOne != -1:
        buketi[buketvertexOne].append(vertexTwo)
      ## they are both in different buket
      elif vertexOne != vertexTwo:
        ### MERGING TWO BUKETS
        lowerIndexBuket = min(buketvertexOne, buketvertexTwo)
        higherIndexBuket = max(buketvertexTwo, buketvertexOne)
        for vertex in buketi[higherIndexBuket]:
          buketi[lowerIndexBuket].append(vertex)
        buketi.remove(buketi[higherIndexBuket]) # deleting this buket
      
      for b in buketi:
        curOutputLine.append(b)
      ## OUTPUT OF CURRENT LINE 
      print(f"{i+1} {curOutputLine}")

      ## SUMMING WEIGHTS OF "г"
      if curOutputLine[1] == "г":
        weight+= curOutputLine[2]
      
      ## VISUALIZING
      ### a,b, weight, color
      GV.addEdge(curOutputLine[0][0], curOutputLine[0][1], curOutputLine[2], curOutputLine[1])
    # PRINT RESULTS
    print(f"Weight: {weight}")

    GV.visualize()
    
    # PRINT IF IT WORKED
    if len(curOutputLine[3]) != vertexAmount:
      print('Doesnt exist')
    else:
      print("Such tree exists")
        

  elif action == FORD_SHORTEST_PATH:
    pass
  elif action == OUTPUT_MATRIX:
    printMatrix(adjMatrix)
  
  input("\nPress any key to continue...\n")