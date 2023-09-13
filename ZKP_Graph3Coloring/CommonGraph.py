# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada
import random  # it is used for the measurements

# The graph is represented by Adjacency Matrix

# In order to create a specific graph, run the function createGraphByAdjMatrix and get the required graph.
# Afterwards, update the value of G to the required graph.

# A 3-coloring graph with 4 vertices and 3 edges
G = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]

# A 3-coloring graph with 10 vertices and 15 edges
G2 = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1, 0, 0, 1, 0], [1, 0, 0, 0, 1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 1], [0, 1, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0, 0, 1, 0, 0]]

# A graph with 5 vertices and 8 edges and which is not 3-coloring
G3 = [[0, 1, 0, 0, 1], [1, 0, 1, 1, 1], [0, 1, 0, 1, 1], [0, 1, 1, 0, 1], [1, 1, 1, 1, 0]]

# Printing the required graph
def createGraphByAdjMatrix():
    #  n is the number of vertices
    #  m is the number of edges
    print("Enter the number of vertices and the number of edges:")
    n, m = map(int, input().split())
    G = [[0 for i in range(n)]for j in range(n)]
    for i in range(m):
        print("Enter 2 vertices that will have an edge between them:")
        u, v = map(int, input().split())
        G[u][v] = 1
        G[v][u] = 1
    print(G)


# A function that gets a path to graph and the index of the first line in the dataset that represent a node, and it returns an adjacency matrix for the given graph
def loadGraphAsAdjMatrix(pathToGraph, indexFirstLineOfData):
    numOfNodes = findNumOfNodes(pathToGraph, indexFirstLineOfData)
    graph = open(pathToGraph)
    lines = graph.readlines()[indexFirstLineOfData:]
    adjMatrix = [[0 for i in range(numOfNodes)]for j in range(numOfNodes)]
    for line in lines:
        u, v = map(int, line.split())
        adjMatrix[u][v] = 1
        adjMatrix[v][u] = 1
    return adjMatrix


# A function that gets a path to graph and the index of the first line in the dataset that represent a node, and it returns the number of nodes in the given graph
def findNumOfNodes(pathToGraph, indexFirstLineOfData):
    graph = open(pathToGraph)
    lines = graph.readlines()[indexFirstLineOfData:]
    maxNode = -1
    for line in lines:
        u, v = map(int, line.split())
        maxNode=max(u, v, maxNode)
    numOfNodes = maxNode + 1  # the nodes are numbered from 0
    return numOfNodes


# Return the required graph
def getCommonGraph():
    # return G
    return G2
    # return G3

    # graphFacebook = loadGraphAsAdjMatrix("facebook_combined.txt", 0)  # A graph with 4039 nodes and 88234 edges
    # return graphFacebook

    # graphP2PGnutella = loadGraphAsAdjMatrix("p2p-Gnutella04.txt", 4)  # A graph with 10879 nodes and 39994 edges
    # return graphP2PGnutella

    # subgraphFacebook = loadCheckingGraphAsAdjMatrix("facebook_combined_NumEdges_88000.txt")  # we ran the protocol for a lot of subgraphs for the measurements (effect of the number of edges)
    # return subgraphFacebook

    # subgraphP2PGnutella = loadCheckingGraphAsAdjMatrix("p2p-Gnutella04_NumNodes_10000.txt")  # we ran the protocol for a lot of subgraphs for the measurements (effect of the number of nodes)
    # return subgraphP2PGnutella


# ***************************
# Functions for measurements:
# ***************************
# A function that gets a path to original graph, the index of the first line in the dataset that represent a node, and the required num of edges
# It creates a new sub-graph of the original graph with the required number of edges
def createCheckingGraphByEdges(pathToOriginalGraph, indexFirstLineOfData, reqNumEdges):
    graph = open(pathToOriginalGraph)
    lines = graph.readlines()[indexFirstLineOfData:]
    random_lines = random.sample(lines, reqNumEdges)
    name = pathToOriginalGraph.split(".txt")[0]+"_NumEdges_"+str(reqNumEdges)
    numOfNodes = findNumOfNodes(pathToOriginalGraph, indexFirstLineOfData)
    writeSubgraphToFile(random_lines, name, numOfNodes)

# A function that gets a path to original graph, the index of the first line in the dataset that represent a node, and the required num of nodes
# It creates a new sub-graph of the original graph with the required number of nodes
def createCheckingGraphByNodes(pathToOriginalGraph, indexFirstLineOfData, reqNumNodes):
    graph = open(pathToOriginalGraph)
    lines = graph.readlines()[indexFirstLineOfData:]
    reqLines = []
    for line in lines:
        u, v = map(int, line.split())
        if u < reqNumNodes and v < reqNumNodes:
            reqLines.append(line)
    name = pathToOriginalGraph.split(".txt")[0]+"_NumNodes_"+str(reqNumNodes)
    writeSubgraphToFile(reqLines, name, reqNumNodes)


# A function that get a list of sub-graphs and the number of nodes (n).
# It outputs to text file the value of n, the number of sub-graphs (count) and the edges of each sub-graph
def writeSubgraphToFile(random_lines, name, numOfNodes):
    filename = f"{name}.txt"
    with open(filename, "w") as file:
        file.write(str(numOfNodes)+"\n")  # the first line will have the number of nodes in the original graph
        for line in random_lines:
            file.write(line)
    return 0


# A function that gets a path to sub-graph, and it returns an adjacency matrix for the given graph
def loadCheckingGraphAsAdjMatrix(pathToSubGraph):
    graph = open(pathToSubGraph)
    lines = graph.readlines()
    numOfNodes = lines[0]
    numOfNodes = int(numOfNodes)

    lines = lines[1:]  # indexFirstLineOfData=1
    adjMatrix = [[0 for i in range(numOfNodes)]for j in range(numOfNodes)]
    for line in lines:
        u, v = map(int, line.split())
        adjMatrix[u][v] = 1
        adjMatrix[v][u] = 1
    return adjMatrix

#if __name__ == '__main__':
#    createGraphByAdjMatrix()

#    for i in range(11):
#        createCheckingGraphByEdges("facebook_combined.txt", 0, (i+1)*8000)

#    for i in range(10):
#        createCheckingGraphByNodes("p2p-Gnutella04.txt", 4, (i+1)*1000)
