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

LETTER_TO_INDEX = {}
INDEX_TO_LETTER = {}

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
        plt.vertex("off")
        plt.tight_layout()
        plt.show()

def createLetterToIndexDict(vertices, isSorted = False):
  if not isSorted:
    vertices = sorted(vertices)
  i = 0
  for vertex in vertices:
    LETTER_TO_INDEX[vertex] = i
    i+=1
def createIndexToLetter(vertices, isSorted = False):
  if not isSorted:
    vertices = sorted(vertices)
  i = 0
  for vertex in vertices:
    INDEX_TO_LETTER[i] = vertex
    i+=1

# letter To Index
def letterToIndex(letter): 
  # ord(char) returns ASCII of char
  # chr(num) returns char 
  # ASCII : a b c d e f g h i j k l m n o p q r s t u v w x y z 
  #return ord(letter.lower())-97 # because a is 97 => so a will be 0 , b 1 and etc. 
  return LETTER_TO_INDEX[letter]
# Index to letter
def indexToLetter(index): 
  # ord(char) returns ASCII of char
  # chr(num) returns char 
  # ASCII : a b c d e f g h i j k l m n o p q r s t u v w x y z 
  #return chr(index+97) # because a is 97 => so a will be 0 , b 1 and etc. 
  return INDEX_TO_LETTER[index]
# alphabetically
def sortvertex (a,b):
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
def sortEdges(edges):
  # First sorted by first vertex letter, then by second, then by weight 
  return sorted(sorted(sorted(edges, key= lambda x: x[0]), key=lambda x: x[1]), key=lambda x : x[2])
def edgesToAdjMatrix(vertices, edges, isSorted = False):
  if not isSorted:
    edges = sortEdges(edges) # Safe redundancy
    vertices=sorted(vertices)
  
  # the order of letter is in letterToIndex()
  cols_count = rows_count = len(vertices)
  adjMatrix = [[0 for x in range(cols_count)] for x in range(rows_count)] 
  for edge in edges:
    vertexOne = edge[0]
    vertexTwo = edge[1]
    weight = edge[2]
    adjMatrix[letterToIndex(vertexOne)][letterToIndex(vertexTwo)] = weight
  return adjMatrix
    
def printMatrix(adjMatrix, startingLetter=None, letterOrder=None):
  # the order of letter is in letterToIndex
  maxNumLength = len(str(np.amax(adjMatrix)))
  dashesMultiplier = maxNumLength + 1 # because we also have | symbol per each number and not number too
  dashesChar = '—' * dashesMultiplier
  def spacesChar(numLen):
    return ' ' * (maxNumLength-numLen)
  


  # Header:
  headerStr = spacesChar(0) + '|'
  headerDashesStr = dashesChar
  for i in range(len(adjMatrix[0])):
    headerStr += f"{indexToLetter(i)}{spacesChar(len(indexToLetter(i)))}|"
    headerDashesStr += dashesChar
  print(headerStr)
  print(headerDashesStr)


  if startingLetter != None:
    pass # TODO: write first then exclude
  else:
    for i in range(len(adjMatrix)): # rows amount (строки)
      outputStr = f'{indexToLetter(i)}{spacesChar(len(indexToLetter(i)))}|'
      dashesStr = dashesChar
      for j in range(len(adjMatrix[0])): #  columns amount (столбцы)
        outputStr += f'{adjMatrix[i][j]}{spacesChar(len(str(adjMatrix[i][j])))}|'
        dashesStr += dashesChar
      print(outputStr)
      print(dashesStr)

        


# Some variables for everything
G = GraphVisualization() 
edges=[]            # [[vertexOne, vertexTwo, Weight], ...]
edges_colored=[]
vertexAmount=0
amountOfedges = 0
adjacencyMatrix = []
vertices_ = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'f', 'g', 'h', 'k', 's', 'm', 'n', 't']
edges_ = [['b', 'a', 529], ['a', 's', 1], ['c', 'a', 3]]

createLetterToIndexDict(vertices_)
createIndexToLetter(vertices_)

printMatrix(edgesToAdjMatrix(vertices_, edges_))

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

# FORMATTING DATA BEFORE DOING ANYTHING AS IT IS EXPECTED TO BE
edges_colored=edges
edges = sortEdges(edges)
vertices = sorted(vertices)
# Deleting duplicates
vertices = list(set(vertices)) 

createIndexToLetter(vertices)
createLetterToIndexDict(vertices)

## Main loop to build several graphs on one set of edges
while (True):
  ## graph type
  graphType = int(input(f"Какой граф нужно построить:\n "
                    f"{MINIMAL_COVERING_TREE}.Минимальное покрывающее дерево."
                    f"\n{MAXIMUM_COVERING_TREE}.Максимальное покрывающее дерево.\n"
                    f"{FORD_SHORTEST_PATH}. Дерево кратчайших путей по Форду.\n"))
  # SORTING INDICES BY edges WEIGHT
  index = 0
  edges_weights = [x[2] for x in edges]
  print(edges_weights)
  sorted_indices = []
  if graphType == MINIMAL_COVERING_TREE  or graphType == MAXIMUM_COVERING_TREE:
    if graphType==MINIMAL_COVERING_TREE:
      sorted_indices = np.argsort(edges_weights)
    elif graphType==MAXIMUM_COVERING_TREE:
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
      G.addEdge(curOutputLine[0][0], curOutputLine[0][1], curOutputLine[2], curOutputLine[1])
    # PRINT RESULTS
    print(f"Weight: {weight}")

    G.visualize()
    
    # PRINT IF IT WORKED
    if len(curOutputLine[3]) != vertexAmount:
      print('Doesnt exist')
    else:
      print("Such tree exists")
        
    input("\nPress any key to continue...\n")
  elif graphType == FORD_SHORTEST_PATH:
    pass