# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada

# coloring[i] is the color of the vertex i, each of the value 1,2,3 represents a different color
# In order to use a specific coloring, update the value of coloring array to the required coloring
coloring = [1, 2, 3, 3]  # the coloring for the graph G
wrongColoring = [1, 1, 1, 2]  # a wrong coloring for G (if the verifier will choose the edges (0,1) or (0,2), it will reject.

coloring2 = [2, 1, 2, 1, 2, 1, 3, 2, 3, 3]  # the coloring for the graph G2
coloring3 = [2, 2, 1, 2, 2]  # the coloring for the graph G3 (not 3-coloring), it will reject in probability of 5/8

coloringForFacebookGraph = [1 for i in range(4039)]  # A wrong coloring for facebookGraph
coloringForP2PGnutellaGraph = [1 for i in range(10879)]  # A wrong coloring for P2PGnutellaGraph

coloringForP2PGnutellaSubgraph = [1 for i in range(10000)]  # A wrong coloring for P2PGnutellaSubgraph (changing for each subgraph)

# Return the private coloring (regarding to the required graph)
def getPrivateColoring():
    return coloring2  # coloringForP2PGnutellaSubgraph#coloringForP2PGnutellaGraph#coloringForFacebookGraph#coloring3#coloring2#wrongColoring#coloring
