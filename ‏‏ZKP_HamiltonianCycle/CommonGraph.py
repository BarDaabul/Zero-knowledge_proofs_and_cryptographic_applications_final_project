# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada
import random  # it is used for the measurements

# The graph is represented by Adjacency Matrix

# In order to create a specific graph, run the function createDirectedGraphByAdjMatrix and get the required graph.
# Afterwards, update the value of M to the required graph.

# A directed graph with hamiltonian cycle which has 4 vertices and 5 edges
M = [[0, 0, 0, 1], [1, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]

# A directed graph with hamiltonian cycle which has 20 vertices and 60 edges
M2 = [[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]]

# A directed graph with no hamiltonian cycle which has 5 vertices and 6 edges
M3 = [[0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 1, 0, 0]]


# Printing the required graph
def createDirectedGraphByAdjMatrix():
    #  n is the number of vertices
    #  m is the number of edges
    print("Enter the number of vertices and the number of edges:")
    n, m = map(int, input().split())
    G = [[0 for i in range(n)]for j in range(n)]
    for i in range(m):
        print("Enter 2 vertices (u and v) so that there will be an edge from u to v:")
        u, v = map(int, input().split())
        G[u][v] = 1
    print(G)


# A function that gets a path to directed graph and the index of the first line in the dataset that represent a node, and it returns an adjacency matrix for the given graph
def loadDirectedGraphAsAdjMatrix(pathToGraph, indexFirstLineOfData):
    numOfNodes = findNumOfNodes(pathToGraph, indexFirstLineOfData)
    graph = open(pathToGraph)
    lines = graph.readlines()[indexFirstLineOfData:]
    adjMatrix = [[0 for i in range(numOfNodes)]for j in range(numOfNodes)]
    for line in lines:
        u, v = map(int, line.split())
        adjMatrix[u][v] = 1
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
    # return M
    return M2
    # return M3

    # subgraphFacebook = loadCheckingDirectedGraphAsAdjMatrix("facebook_combined_reduced_NumEdges_9000.txt")  # we ran the protocol for a lot of subgraphs for the measurements (effect of the number of edges)
    # return subgraphFacebook

    # subgraphP2PGnutella = loadCheckingDirectedGraphAsAdjMatrix("p2p-Gnutella04_NumNodes_1500.txt")  # we ran the protocol for a lot of subgraphs for the measurements (effect of the number of nodes)
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
def loadCheckingDirectedGraphAsAdjMatrix(pathToSubGraph):
    graph = open(pathToSubGraph)
    lines = graph.readlines()
    numOfNodes = lines[0]
    numOfNodes = int(numOfNodes)

    lines = lines[1:]  # indexFirstLineOfData=1
    adjMatrix = [[0 for i in range(numOfNodes)]for j in range(numOfNodes)]
    for line in lines:
        u, v = map(int, line.split())
        adjMatrix[u][v] = 1
    return adjMatrix


# if __name__ == '__main__':

#    createDirectedGraphByAdjMatrix()

# ***************************************************************************************************************
# graphs for finding the metrics as a function of the number of nodes and the number of edges (for bit=0 and bit=1 separately)

#    # a reduced graph of facebook with 1000 nodes (it has 9890 edges), that will use for checking the effect of the number of edges. The file of the reduced graph: facebook_combined_reduced.txt
#    createCheckingGraphByNodes("facebook_combined.txt", 0, 1000)

#    for i in range(9):
#        createCheckingGraphByEdges("facebook_combined_reduced.txt", 1, (i+1)*1000)

#    for i in range(10):
#        createCheckingGraphByNodes("p2p-Gnutella04.txt", 4, (i+1)*150)

# ************************************************************************************************************
# graphs for finding the average weighted metrics as a function of the number of nodes and the number of edges

#    # a reduced graph of facebook with 400 nodes (it has 3062 edges), that will use for checking the effect of the number of edges. The file of the reduced graph: facebook_combined_for_avg_weight_metrics.txt
#    createCheckingGraphByNodes("facebook_combined.txt", 0, 400)

#    for i in range(6):
#        createCheckingGraphByEdges("facebook_combined_for_avg_weight_metrics.txt", 1, (i+1)*500)

#    for i in range(6):
#        createCheckingGraphByNodes("p2p-Gnutella04.txt", 4, (i+1)*100)
