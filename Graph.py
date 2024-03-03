import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt 
import json
from datetime import datetime
from collections import defaultdict
import math
import sys
import os

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
  EMPTY_MATRIX_ITEM_SYMBOL = math.inf # how it is stored in matrix itself
  TXT_FOLDER_RELATIVE_PATH = "TXTS/"
  TXT_FOLDER_ABSOLUTE_PATH =  "TXTS"
  EDGE_TXT_PREFIX = "edge-"
  VERTICES_TXT_PREFIX = "vertices-"
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
    # First sorted by first vertex letter
    return sorted(edges, key= lambda x: x[0])
  def edgesToAdjMatrix(vertices, edges, isSorted = False):
    if not isSorted:
      edges = Graph.sortEdges(edges) # Safe redundancy
      vertices=sorted(vertices)
    
    # the order of letter is in letterToIndex()
    cols_count = rows_count = len(vertices)
    adjMatrix = [[Graph.EMPTY_MATRIX_ITEM_SYMBOL for x in range(cols_count)] for x in range(rows_count)] 
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
  
  def createMatrixD(rows = None, columns = None, rowsNames=[], columnsNames=[]):
    # They are different to Adj matrices, because they are произвольные
    if len(rowsNames) == 0 and len(columnsNames==0):
      raise("When creating matrix you have to pass rowsNames / columnsNames.")
    matrix = {}
    Graph.appendMatrixD(matrix, rowsToAppend=rows, columnsToAppend=columns, columnsNames=columnsNames, rowsNames=rowsNames)
    return matrix
  def getMatrixRow(matrix, rowName):
    row = []
    columnNames = Graph.getMatrixColumnNames(matrix)

    
    for j in range (len(columnNames)):
      row.append(matrix[rowName, columnNames[j]])
    return row
    
    
  def getMatrixColumn(matrix, columnName):
    column = []
    rowsNames = Graph.getMatrixRowNames(matrix)
    
    for i in range (len(rowsNames)):
      column.append(matrix[rowsNames[i], columnName])
    return column
  
  def getRowNameOfMaxInColumn(matrix, columnName):
    column = Graph.getMatrixColumn(matrix, columnName)
    onlyIntColumn=[]
    for c in column:
      if type(c) != type(1) or type(c) == type(math.inf):
        continue
      else:
        onlyIntColumn.append(c)
    if len(onlyIntColumn) != 0:
      maxIndex = column.index(max(onlyIntColumn))
      return Graph.getMatrixRowNames(matrix)[maxIndex]
    else:
      return None

  def getRowNameOfMinInColumn(matrix, columnName):
    column = Graph.getMatrixColumn(matrix, columnName)
    onlyIntColumn=[]
    for c in column:
      if type(c) != type(1) or type(c) == type(math.inf):
        continue
      else:
        onlyIntColumn.append(c)
    if len(onlyIntColumn) != 0:
      maxIndex = column.index(min(onlyIntColumn))
      return Graph.getMatrixRowNames(matrix)[maxIndex]
    else:
      return None

  def getColumnNameOfMaxInRow(matrix, rowName):
    row = Graph.getMatrixRow(matrix, rowName)
    onlyIntRow =[]
    for c in row:
      if type(c) != type(1) or type(c) == type(math.inf):
        continue
      else:
        onlyIntRow.append(c)
    if (len(onlyIntRow) != 0):
      maxIndex = row.index(max(onlyIntRow))
      return Graph.getMatrixColumnNames(matrix)[maxIndex]
    else:
      return None

  def getColumnNameOfMinInRow(matrix, rowName):
    row = Graph.getMatrixRow(matrix, rowName)
    onlyIntRow =[]
    for c in row:
      if type(c) != type(1) or type(c) == type(math.inf):
        continue
      else:
        onlyIntRow.append(c)
    if (len(onlyIntRow) != 0):
      maxIndex = row.index(min(onlyIntRow))
      return Graph.getMatrixColumnNames(matrix)[maxIndex]
    else:
      return None
  def getLastNum(rowOrColumnArray):
    # from 8 to 0 inclusive with a step of -1
    for i in range(len(rowOrColumnArray)-1, -1, -1):
      if i == '-' or i == '/' or i == Graph.EMPTY_MATRIX_ITEM_SYMBOL:
        continue
      else:
        return i


  def getMatrixColumnNames(matrix):
    columnNames = []
    sets = list(matrix)
    for o in sets:
      if (list(o)[1] not in columnNames): columnNames.append(list(o)[1])
    return columnNames
  def getMatrixRowNames(matrix):
    rowsNames = []
    sets = list(matrix)
    for o in sets:
      if (list(o)[0] not in rowsNames): rowsNames.append(list(o)[0])
    return rowsNames
    
    
  def appendMatrixD(matrix, rowsToAppend = None, columnsToAppend =None, columnsNames=None, rowsNames=None): 
    # YOU HAVE TO PASS ROWS/COLUMNS NAME WHEN CREATING
    if(rowsNames == None):rowsNames=Graph.getMatrixRowNames(matrix) 
    if(columnsNames==None): columnsNames=Graph.getMatrixColumnNames(matrix)
    # add column or row to any matrix
    # it is assumed that added row or column has a name of it as a first element 
    # verificating that data is in double array:
    if rowsToAppend != None:
      if type(rowsToAppend[0]) != type(rowsToAppend): rowsToAppend = list(rowsToAppend)
    if columnsToAppend != None:
      if type(columnsToAppend[0]) != type(columnsToAppend): columnsToAppend = list(columnsToAppend)


    if rowsToAppend != None and columnsToAppend != None:
      for i in range(len(rowsToAppend)):
          # the first element of this row
          rowName = rowsToAppend[i][0] 
          # current row we are iterating thru
          row = rowsToAppend[i] 
          # except 1st (index 0) element because it is name
          for j in range(1,len(rowsToAppend[i])): 
            # we are going thru every column first variables which is its name
            matrix[rowName, columnsToAppend[j-1][0]] = row[j] 
      for i in range(len(columnsToAppend)):
          # the first element of this row
          columnName = columnsToAppend[i][0] 
          # current row we are iterating thru
          column = columnsToAppend[i] 
          # except 1st (index 0) element because it is name
          for j in range(1,len(columnsToAppend[i])): 
            # j-1 because j goes 1, 2 ... and we need from first column
            matrix[rowsToAppend[j-1][0], columnName] = column[j] 

    else:
      if rowsToAppend !=None:
        for i in range(len(rowsToAppend)):
          # the first element of this row
          rowName = rowsToAppend[i][0] 
          # current row we are iterating thru
          row = rowsToAppend[i] 
          # except 1st (index 0) element because it is name
          for j in range(1,len(rowsToAppend[i])): 
            # j-1 because j goes 1, 2 ... and we need from first column
            matrix[rowName, columnsNames[j-1]] = row[j] 
      if columnsToAppend != None:
        for i in range(len(columnsToAppend)):
          # the first element of this row
          columnName = columnsToAppend[i][0] 
          # current row we are iterating thru
          column = columnsToAppend[i] 
          # except 1st (index 0) element because it is name
          for j in range(1,len(columnsToAppend[i])): 
            # j-1 because j goes 1, 2 ... and we need from first column
            matrix[rowsNames[j-1], columnName] = column[j] 
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
        adjMatrix[v1,v2] = Graph.EMPTY_MATRIX_ITEM_SYMBOL
    for edge in edges:
      vertexOne = edge[0]
      vertexTwo = edge[1]
      weight = edge[2]
      adjMatrix[vertexOne, vertexTwo] = weight
    return adjMatrix

  def printMatrix(adjMatrix, startingLetter=None, letterOrder=None, emptySymbol=''):
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
          adjMatrixValue = adjMatrix[i][j] 
          # To avoid ugly infs
          if adjMatrixValue == math.inf: adjMatrixValue = emptySymbol

          outputStr += f'{adjMatrixValue}{spacesChar(len(str(adjMatrixValue)))}|'
          dashesStr += dashesChar
        print(outputStr)
        print(dashesStr)

  def printMatrixDict(adjMatrix, startingLetter=None, letterOrder=None, emptySymbol = ''):
    # !!! adjMatrix sets should be sorted 
    sets = list(adjMatrix)
    rowVertices = []
    columnVertices = []
    for o in sets:
      if (list(o)[0] not in rowVertices): rowVertices.append(list(o)[0])
      if (list(o)[1] not in columnVertices): columnVertices.append(list(o)[1])
    rowsAmount = len(rowVertices)
    columnsAmount = len(columnVertices)
    # to find the number after infinity
    val = list(set(list(adjMatrix.values())))
    valInt=[]
    for i in val:
      if type(i) != type(1) or type(i) == type(math.inf):
        continue
      else:
        valInt.append(i)
    if (len(valInt)!= 0):
      valInt.sort() # What to do with - and / and etc 
      maxNumLength = len(str(valInt[-1]))
    else:
      # We only have left infinities
      maxNumLength=len(emptySymbol)
    dashesMultiplier = maxNumLength + 1 # because we also have | symbol per each number and not number too
    dashesChar = '—' * dashesMultiplier
    def spacesChar(numLen):
      return ' ' * (maxNumLength-numLen)
    

    # Header:
    headerStr = spacesChar(0) + '|'
    headerDashesStr = dashesChar
    for i in columnVertices:
      headerStr += f"{i}{spacesChar(len(i))}|"
      headerDashesStr += dashesChar
    print(headerStr)
    print(headerDashesStr)


    if startingLetter != None:
      pass # TODO: write first then exclude
    else:
      for i in rowVertices: 
        outputStr = f'{i}{spacesChar(len(i))}|'
        dashesStr = dashesChar
        for j in columnVertices: 
          adjMatrixValue = adjMatrix[i,j]
          if adjMatrixValue == math.inf: adjMatrixValue = emptySymbol # so it wouldnt look so messy
          outputStr += f'{adjMatrixValue}{spacesChar(len(str(adjMatrixValue)))}|'
          dashesStr += dashesChar
        print(outputStr)
        print(dashesStr)

  def printMatrixToFile(adjMatrix):
    fileName = f"{Graph.TXT_FOLDER_RELATIVE_PATH}{Graph.SAME_SECOND_NUM}adjMatrix-" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    with open(fileName, 'w') as f:
      sys.stdout = f
      Graph.printMatrix(adjMatrix)
      sys.stdout = Graph.ORIGINAL_STDOUT
    Graph.SAME_SECOND_NUM+=1
  def printMatrixDictToFile(adjMatrix):
    fileName = f"{Graph.TXT_FOLDER_RELATIVE_PATH}{Graph.SAME_SECOND_NUM}adjMatrix-" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
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
  #   with open(TXT_FOLDER_RELATIVE_PATH + FILE_NAME, 'w') as outfile:
  #       json.dump(adjMatrix, outfile)
  def exportEdges(edges):
    FILE_NAME = f"{Graph.TXT_FOLDER_RELATIVE_PATH}{Graph.SAME_SECOND_NUM}{Graph.EDGE_TXT_PREFIX}" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    # dump the dict contents using json 
    with open(FILE_NAME, 'w') as outfile:
        json.dump(edges, outfile)
    Graph.SAME_SECOND_NUM+=1
  def exportVertices(vertices):
    FILE_NAME = f"{Graph.TXT_FOLDER_RELATIVE_PATH}{Graph.SAME_SECOND_NUM}{Graph.VERTICES_TXT_PREFIX}" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') +".txt"
    # dump the dict contents using json 
    with open(FILE_NAME, 'w') as outfile:
        json.dump(vertices, outfile)
    Graph.SAME_SECOND_NUM+=1
  def drawAnyGraph():
    pass
  def getAvailableFiles():
    return [Graph.TXT_FOLDER_RELATIVE_PATH+ f for f in os.listdir(Graph.TXT_FOLDER_RELATIVE_PATH)]
  def getAvailableEdgeFile():
    files = Graph.getAvailableFiles()
    edgeFiles = []
    for file in files:
      if Graph.EDGE_TXT_PREFIX in file:
        edgeFiles.append(file)
    
    return edgeFiles
  def getAvailableVerticesFile():
    files = Graph.getAvailableFiles()
    verticesFiles = []
    for file in files:
      if Graph.VERTICES_TXT_PREFIX in file:
        verticesFiles.append(file)
    
    return verticesFiles