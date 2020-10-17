"""
Author: Rachael Judy
Date: 10/16/2020
Purpose: HW 7 BFS and DFS
Demonstrate the Breadth first search and depth first search on graph type.
Use topological sort on graph

"""
import queue
import sys
from collections import defaultdict
from collections import deque


# vertex class associated with each vertex in the graph
class Vertex:
    def __init__(self):
        self.color = 'W'
        self.pred = None

        # for BFS
        self.distance = 1000000

        # for DFS
        self.dtime = 0
        self.ftime = 0


# Graph class contains graph of each vertex value and then
# a dictionary of a Vertex object for each value
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # composed of vertex values
        self.vertexDict = {}  # contains properties of each vertex
        self.topo_list = deque()

    # add an edge to the graph and create the property entry in dictionary
    def addEdge(self, u, v):
        # add to graph
        self.graph[u].append(v)

        # add property object
        self.vertexDict[u] = Vertex()
        self.vertexDict[v] = Vertex()

    # get the list of vertices
    def getVertices(self):
        return self.graph.keys()

    # get the collection of adjacencies for the vertex
    def getAdjacencies(self, ver):
        return self.graph[ver]

    #
    def computeTranspose(self):
        transpose = Graph()
        for v in self.getVertices():
            for u in self.getAdjacencies(v):
                transpose.addEdge(u, v)
        return transpose

    def print(self):
        for v in self.getVertices():
            print(v, end='->')
            print(self.getAdjacencies(v))
        print()


def BFS(G, s):
    for v in G.getVertices():
        if G.vertexDict[v] != G.vertexDict[s]:
            G.vertexDict[v].color = 'W'
            G.vertexDict[v].distance = 1000000
            G.vertexDict[v].pred = None

    G.vertexDict[s].color = 'G'
    G.vertexDict[s].distance = 0
    G.vertexDict[s].pred = None

    Q = queue.Queue()
    Q.put(s)
    while not Q.empty():
        u = Q.get()
        for v in G.graph[u]:
            if G.vertexDict[v].color == 'W':
                G.vertexDict[v].color = 'G'
                G.vertexDict[v].distance = G.vertexDict[u].distance + 1
                G.vertexDict[v].pred = u
                Q.put(v)

        G.vertexDict[u].color = 'B'

# print the path between two vertices
def Print_Path(G, s, v):
    if v == None:
        return

    if v == s:
        print(s, end=' ')
    elif G.vertexDict[v].pred == None:
        print("no path from " + s + " to " + v + " exists")
    else:
        Print_Path(G, s, G.vertexDict[v].pred)
        print(v, end=' ')


# function for printing the results of BFS
def Print_BFS(graph, vertex):
    for ver in graph.getVertices():
        print("The path from " + vertex + " to " + ver +
              " (" + str(graph.vertexDict[ver].distance) + ", "
              + str(graph.vertexDict[ver].color) + ", "
              + str(graph.vertexDict[ver].pred)
              + ") is: ", end='')
        Print_Path(graph, vertex, ver)
        print()
    print()


# function for search depth first
time = 0
def DFS(G):
    # reset all attributes
    for u in G.getVertices():
        G.vertexDict[u].color = 'W'
        G.vertexDict[u].pred = None

    # visit each and color
    global time
    time = 0
    for u in G.getVertices():
        if G.vertexDict[u].color == 'W':
            DFS_Visit(G, u)


# recursively uesd by DFS
def DFS_Visit(G, u):
    global time
    time = time + 1

    # store start time and color the working vertex gray
    G.vertexDict[u].dtime = time
    G.vertexDict[u].color = 'G'

    # go through adjecencies and store predecessors, follow recursively
    for v in G.getAdjacencies(u):
        if G.vertexDict[v].color == 'W':
            G.vertexDict[v].pred = u
            DFS_Visit(G, v)

    # color completed vertices and keep time
    G.vertexDict[u].color = 'B'
    time = time + 1
    G.vertexDict[u].ftime = time
    G.topo_list.appendleft(u)


# print results of DFS
def Print_DFS(graph):
    for ver in graph.getVertices():
        vData = graph.vertexDict[ver]
        print(ver + " (" + str(vData.dtime) + "/" + str(vData.ftime)
              + " " + str(vData.color) + " " + str(vData.pred) + ")")
    print()


# run DFS and populate the topographical listing
def Topological_Sort(graph):
    graph.topo_list.clear()
    DFS(graph)
    return graph.topo_list


def Print_Topo(graph):
    for ver in graph.topo_list:
        vData = graph.vertexDict[ver]
        print(ver + " (" + str(vData.dtime) + "/" + str(vData.ftime)
              + " " + str(vData.color) + " " + str(vData.pred) + ")")
    print()

# create graph from input
filename = "TopoTest1"
if len(sys.argv) == 2:
    filename = sys.argv[1]
# else:  # defaults to one of the provided files left in its directory for testing
#     print("Enter a filename to test as follows: Graph.py <filename>")
#     exit(0)

# open and collect inputs
try:
    file = open(filename, 'r')
except Exception:
    print("Failed to open file.")
    exit(0)
numNodes = int(file.readline())

# create graph here
graph = Graph()
for i in range(numNodes):
    line = file.readline()
    keyValue = line[0]
    if len(line) <= 2:
        graph.graph[keyValue] = []
        graph.vertexDict[keyValue] = Vertex()
    for j in range(1, len(line) - 1):
        graph.addEdge(keyValue, line[j])


# test all graph functions
print("Graph")
graph.print()

print("Transposed Graph")
tp = graph.computeTranspose()
tp.print()

# change vertices index to get the one you want's path
# or change vertices[0] to vertex value of choice
print("BFS")
vertices = [i for i in graph.getVertices()]
BFS(graph, vertices[0])
Print_BFS(graph, vertices[0])

print("DFS")
DFS(graph)
Print_DFS(graph)

print("Topological Sort")
Topological_Sort(graph)
Print_Topo(graph)