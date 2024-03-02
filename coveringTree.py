import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt 

# вершина = vertex / vertices
# дуга = edge / edges

MINIMAL_COVERING_TREE = 1
MAXIMUM_COVERING_TREE = 2

MINIMUM_ORIENTED_FOREST = 3
MAXIMUM_ORIENTED_FOREST = 4

MAXIMUM_ORIENTED_COVERING_TREE = 5
MINIMAL_ORIENTED_COVERING_TREE = 6

FORD_SHORTEST_PATH = 7


MANUAL_INPUT_TYPE = 1
MATRIX_INPUT_TYPE = 2
ORIENTED_MATRIX_INPUT_TYPE = 3

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
          
    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        G = nx.Graph() 

        for edge in self.visual:
          G.add_edge(edge[0], edge[1], weight=edge[2], color=edge[3])

        # u - first v - second, d - data ??
        blue = [(u, v) for (u, v, d) in G.edges(data=True) if d["color"] == "г"]
        orange = [(u, v) for (u, v, d) in G.edges(data=True) if d["color"] == "о"]

        pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=blue, width=6, edge_color="b")
        nx.draw_networkx_edges(
        G, pos, edgelist=orange, width=6, edge_color="r")

        # node labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)



        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

# alphabetically
def sortAxis (a,b):
  first_letter = ""
  second_letter =""
  a = a.lower()
  b = b.lower()
  if a > b:
    second_letter=a
    first_letter=b
  elif a<b:
    second_letter=b
    first_letter=a
  else:
    return a,b
  return first_letter, second_letter

def edgesToAdjMatrix():


# Some variables for everything
G = GraphVisualization() 
rebra=[]
rebra_colored=[]
axisAmount=0
amountOfRebra = 0
adjacencyMatrix = []

# USER INPUT
inputType = int(input(f"Выберите тип ввода:\n "
             f"{MANUAL_INPUT_TYPE}. Ребра типа a b 10.\n "
             f"{MATRIX_INPUT_TYPE}. Ребра по матрице смежности (неориетированный).\n"
             f"{ORIENTED_MATRIX_INPUT_TYPE}. Ребра по матрице смежности (ориентированный).\n"))
if inputType == MANUAL_INPUT_TYPE:
## axis amount
  axisAmount = int(input("Введите кол-во вершин: "))


  print(rebra)
  ## actually inputing rebra 
  print("Вводите ребра в формате a b 10 (первая вершина, вторая, вес). Введите exit чтобы закончить")
  userInput = ""
  while (True):
    userInput = input().split()
    if (userInput == ["exit"]): break
    userInput[2] = int(userInput[2])
    rebra.append(userInput)
elif inputType == MATRIX_INPUT_TYPE:
  axes = input("Введите все вершины через пробел: a b c d ...").split()
  axisAmount = len(axes)
  axisIndex = 0
  for axisOne in axes:
    axesTwoAndWeight = input(f"Введите вершины (кроме {axes[:axisIndex]})которым {axisOne} смежна: ").split()
    axisIndex+=1
    if axesTwoAndWeight == '': continue
    for i in range(0,len(axesTwoAndWeight), 2):
      axisTwo = axesTwoAndWeight[i] 
      weight_ = int(axesTwoAndWeight[i+1])
      rebra.append([axisOne,axisTwo,weight_])
elif inputType == ORIENTED_MATRIX_INPUT_TYPE:
    axes = input("Введите все вершины через пробел: a b c d ...").split()
    axisAmount = len(axes)
    axisIndex = 0
    for axisOne in axes:
      axesTwoAndWeight = input(f"Введите вершины которым {axisOne} смежна: (b 40 c 50 d 20) ").split()
      axisIndex+=1
      if axesTwoAndWeight == '': continue
      for i in range(0,len(axesTwoAndWeight), 2):
        axisTwo = axesTwoAndWeight[i] 
        weight_ = int(axesTwoAndWeight[i+1])
        rebra.append([axisOne,axisTwo,weight_])

rebra_colored=rebra
## Main loop to build several graphs on one set of rebra
while (True):
  ## graph type
  graphType = int(input(f"Какой граф нужно построить:\n "
                    f"{MINIMAL_COVERING_TREE}.Минимальное покрывающее дерево."
                    f"\n{MAXIMUM_COVERING_TREE}.Максимальное покрывающее дерево.\n"
                    f"{FORD_SHORTEST_PATH}. Дерево кратчайших путей по Форду.\n"))
  # SORTING INDICES BY REBRA WEIGHT
  index = 0
  rebra_weights = [x[2] for x in rebra]
  print(rebra_weights)
  sorted_indices = []
  if graphType == MINIMAL_COVERING_TREE  or graphType == MAXIMUM_COVERING_TREE:
    if graphType==MINIMAL_COVERING_TREE:
      sorted_indices = np.argsort(rebra_weights)
    elif graphType==MAXIMUM_COVERING_TREE:
      sorted_indices = np.argsort(rebra_weights)[::-1]

    print("sorted indices : ", sorted_indices)

    output = []
    buketi = []
    curOutputLine=[]
    weight = 0
    # MAIN LOOP BUILDING GRAPH
    
    for i in sorted_indices:
      if len(curOutputLine) > 0:
        if len(curOutputLine[3]) == axisAmount:
          break
      axisOne = rebra[i][0]
      axisTwo = rebra[i][1]
      if axisOne == axisTwo: 
        continue ## This shouldn't be a loop 
      axisOne, axisTwo = sortAxis(axisOne, axisTwo)
      buketAxisOne = -1
      buketAxisTwo = -1
      ## 0,                            1,   2,   3, 4
      ## [вершина, вершина] - ребро, цвет, вес, б1, б2 ... 
      curOutputLine = [[axisOne, axisTwo], "г", rebra[i][2]]
      for buket_i in range(len(buketi)):
        if (axisOne in buketi[buket_i]): buketAxisOne = buket_i
        if (axisTwo in buketi[buket_i]): buketAxisTwo = buket_i
      ## from same buket
      if buketAxisOne == buketAxisTwo and buketAxisOne != -1:
        curOutputLine[1] = "о"
      ## none are from buket
      elif buketAxisOne == -1 and buketAxisTwo == -1:
        curOutputLine[1]="г"
        buketi.append([axisOne, axisTwo]) # new buket created
      ## axisOne in buket and axisTwo is not
      elif buketAxisOne == -1 and buketAxisTwo != -1:
        buketi[buketAxisTwo].append(axisOne)
      ## axisTwo in buket and axisOne is not
      elif buketAxisTwo == -1 and buketAxisOne != -1:
        buketi[buketAxisOne].append(axisTwo)
      ## they are both in different buket
      elif axisOne != axisTwo:
        ### MERGING TWO BUKETS
        lowerIndexBuket = min(buketAxisOne, buketAxisTwo)
        higherIndexBuket = max(buketAxisTwo, buketAxisOne)
        for axis in buketi[higherIndexBuket]:
          buketi[lowerIndexBuket].append(axis)
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
      G.addEdge(curOutputLine[0][0], curOutputLine[0][1], curOutputLine[2], curOutputLine[1])
    # PRINT RESULTS
    print(f"Weight: {weight}")

    G.visualize()
    
    # PRINT IF IT WORKED
    if len(curOutputLine[3]) != axisAmount:
      print('Doesnt exist')
    else:
      print("Such tree exists")
        
    input("\nPress any key to continue...\n")
  elif graphType == FORD_SHORTEST_PATH:
