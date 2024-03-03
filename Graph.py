import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt 
import json
from datetime import datetime
from collections import defaultdict
import math
import sys
def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))
class Graph: 
  SAME_SECOND_NUM = 0 # If we are exporting two files and it is the same second, so the file name wouldnt be the same
  LETTER_TO_INDEX = {}
  INDEX_TO_LETTER = {}
  ORIGINAL_STDOUT = sys.stdout
  EMPTY_MATRIX_SYMBOL = math.inf
  TXT_FOLDER = "TXTS/"
  def createLetterToIndexDict(vertices, isSorted = False):
    if not isSorted:
      vertices = sorted(vertices)
    i = 0
    for vertex in vertices:
      Graph.LETTER_TO_INDEX[vertex] = i
      i+=1
  def createIndexToLetter(vertices, isSorted = False):
    if not isSorted:
      vertices = sorted(vertices)
    i = 0
    for vertex in vertices:
      Graph.INDEX_TO_LETTER[i] = vertex
      i+=1

  # letter To Index
  def letterToIndex(letter): 
    # ord(char) returns ASCII of char
    # chr(num) returns char 
    # ASCII : a b c d e f g h i j k l m n o p q r s t u v w x y z 
    #return ord(letter.lower())-97 # because a is 97 => so a will be 0 , b 1 and etc. 
    return Graph.LETTER_TO_INDEX[letter]
  # Index to letter
  def indexToLetter(index): 
    # ord(char) returns ASCII of char
    # chr(num) returns char 
    # ASCII : a b c d e f g h i j k l m n o p q r s t u v w x y z 
    #return chr(index+97) # because a is 97 => so a will be 0 , b 1 and etc. 
    return Graph.INDEX_TO_LETTER[index]
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
      edges = Graph.sortEdges(edges) # Safe redundancy
      vertices=sorted(vertices)
    
    # the order of letter is in letterToIndex()
    cols_count = rows_count = len(vertices)
    adjMatrix = [[Graph.EMPTY_MATRIX_SYMBOL for x in range(cols_count)] for x in range(rows_count)] 
    for edge in edges:
      vertexOne = edge[0]
      vertexTwo = edge[1]
      weight = edge[2]
      adjMatrix[Graph.letterToIndex(vertexOne)][Graph.letterToIndex(vertexTwo)] = weight
    return adjMatrix

  def edgesToAdjMatrixNestedDict(vertices, edges, isSorted = False):
    if not isSorted:
      edges = Graph.sortEdges(edges) # Safe redundancy
      vertices=sorted(vertices)
    
    # the order of letter is in letterToIndex()
    cols_count = rows_count = len(vertices)
    adjMatrix = nested_dict(2, int)
    for edge in edges:
      vertexOne = edge[0]
      vertexTwo = edge[1]
      weight = edge[2]
      adjMatrix[vertexOne][vertexTwo] = weight
    return adjMatrix

  def edgesToAdjMatrixDict(vertices, edges, isSorted = False):
    if not isSorted:
      edges = Graph.sortEdges(edges) # Safe redundancy
      vertices=sorted(vertices)
    
    # the order of letter is in letterToIndex()
    cols_count = rows_count = len(vertices)
    adjMatrix = {}
    # Initialize adjMatrixDict:
    for v1 in vertices:
      for v2 in vertices:
        adjMatrix[v1,v2] = Graph.EMPTY_MATRIX_SYMBOL
    for edge in edges:
      vertexOne = edge[0]
      vertexTwo = edge[1]
      weight = edge[2]
      adjMatrix[vertexOne, vertexTwo] = weight
    return adjMatrix

  def printMatrix(adjMatrix, startingLetter=None, letterOrder=None):
    # the order of letter is in letterToIndex
    rowsAmount = len(adjMatrix)
    columnsAmount = len(adjMatrix[0])

    maxNumLength = len(str(np.amax(adjMatrix)))
    dashesMultiplier = maxNumLength + 1 # because we also have | symbol per each number and not number too
    dashesChar = '—' * dashesMultiplier
    def spacesChar(numLen):
      return ' ' * (maxNumLength-numLen)
    

    # Header:
    headerStr = spacesChar(0) + '|'
    headerDashesStr = dashesChar
    for i in range(len(adjMatrix[0])):
      headerStr += f"{Graph.indexToLetter(i)}{spacesChar(len(Graph.indexToLetter(i)))}|"
      headerDashesStr += dashesChar
    print(headerStr)
    print(headerDashesStr)


    if startingLetter != None:
      pass # TODO: write first then exclude
    else:
      for i in range(rowsAmount): # rows amount (строки)
        outputStr = f'{Graph.indexToLetter(i)}{spacesChar(len(Graph.indexToLetter(i)))}|'
        dashesStr = dashesChar
        for j in range(columnsAmount): #  columns amount (столбцы)
          outputStr += f'{adjMatrix[i][j]}{spacesChar(len(str(adjMatrix[i][j])))}|'
          dashesStr += dashesChar
        print(outputStr)
        print(dashesStr)

  def printMatrixDict(adjMatrix, startingLetter=None, letterOrder=None):
    sets = list(adjMatrix)
    vertices = []
    for o in sets:
      if (list(o)[0] not in vertices): vertices.append(list(o)[0])
      if (list(o)[1] not in vertices): vertices.append(list(o)[1])
    # to find the number after infinity
    val = list(set(list(adjMatrix.values())))
    val.sort()
    maxNumLength = len(str(val[-2]))
    dashesMultiplier = maxNumLength + 1 # because we also have | symbol per each number and not number too
    dashesChar = '—' * dashesMultiplier
    def spacesChar(numLen):
      return ' ' * (maxNumLength-numLen)
    

    # Header:
    headerStr = spacesChar(0) + '|'
    headerDashesStr = dashesChar
    for i in vertices:
      headerStr += f"{i}{spacesChar(len(i))}|"
      headerDashesStr += dashesChar
    print(headerStr)
    print(headerDashesStr)


    if startingLetter != None:
      pass # TODO: write first then exclude
    else:
      for i in vertices: 
        outputStr = f'{i}{spacesChar(len(i))}|'
        dashesStr = dashesChar
        for j in vertices: 
          adjMatrixValue = adjMatrix[i,j]
          if adjMatrixValue == math.inf: adjMatrixValue = '' # so it wouldnt look so messy
          outputStr += f'{adjMatrixValue}{spacesChar(len(str(adjMatrixValue)))}|'
          dashesStr += dashesChar
        print(outputStr)
        print(dashesStr)

  def printMatrixToFile(adjMatrix):
    fileName = f"{Graph.SAME_SECOND_NUM}adjMatrix-" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    with open(fileName, 'w') as f:
      sys.stdout = f
      Graph.printMatrix(adjMatrix)
      sys.stdout = Graph.ORIGINAL_STDOUT
    Graph.SAME_SECOND_NUM+=1
  def printMatrixDictToFile(adjMatrix):
    fileName = f"{Graph.SAME_SECOND_NUM}adjMatrix-" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    with open(fileName, 'w') as f:
      sys.stdout = f
      Graph.printMatrixDict(adjMatrix)
      sys.stdout = Graph.ORIGINAL_STDOUT
    Graph.SAME_SECOND_NUM+=1
  # def importAdjMatrix():
  #   pass
  def importFile(fileName):
    file_text = ''
    with open(fileName, 'rt') as file_placeholder:
        lines = file_placeholder.readlines()
        file_text = ''.join(lines)  # This provides the whole file data as string
    # Load as json
    return json.loads(file_text)
  # def importVertices(fileName):
  #   file_text = ''
  #   with open(fileName, 'rt') as file_placeholder:
  #       lines = file_placeholder.readlines()
  #       file_text = ''.join(lines)  # This provides the whole file data as string
  #   # Load as json
  #   return json.loads(file_text)
  # def exportAdjMatrix(adjMatrix):
  #   FILE_NAME = "adjMatrix" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') +".txt"
  #   # dump the dict contents using json 
  #   with open(TXT_FOLDER + FILE_NAME, 'w') as outfile:
  #       json.dump(adjMatrix, outfile)
  def exportEdges(edges):
    FILE_NAME = f"{Graph.SAME_SECOND_NUM}edges-" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    # dump the dict contents using json 
    with open(FILE_NAME, 'w') as outfile:
        json.dump(edges, outfile)
    Graph.SAME_SECOND_NUM+=1
  def exportVertices(vertices):
    FILE_NAME = f"{Graph.SAME_SECOND_NUM}vertices-" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    # dump the dict contents using json 
    with open(FILE_NAME, 'w') as outfile:
        json.dump(vertices, outfile)
    Graph.SAME_SECOND_NUM+=1
  def printAvailableFiles():
    pass
  def drawAnyGraph():
    pass