# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada

# hamiltonianCycle has the visited nodes in the order of the required path
# In order to use a specific hamiltonian cycle, update the value of the array to the required path
hamiltonianCycle = [0, 3, 1, 2, 0]  # a hamiltonian cycle in M
wrongPath = [0, 3, 1, 0]  # a wrong path for M (not hamiltonian cycle)

hamiltonianCycle2 = [0, 1, 2, 9, 8, 7, 6, 5, 14, 13, 12, 19, 15, 16, 17, 18, 10, 11, 3, 4, 0]  # an hamiltonian cycle in M2
hamiltonianCycle3 = [0, 2, 3, 4, 2]  # a wrong path for M3 (M3 doesn't have a hamiltonian cycle)

# A path for reducedFacebookGraph
pathForFacebookGraph = [i for i in range(1000)]  # It is 400 for facebook_combined_for_avg_weight_metrics
pathForFacebookGraph.append(0)

# A path for P2PGnutellaSubgraph (changing for each subgraph)
pathForP2PGnutellaSubgraph = [i for i in range(1500)]
pathForP2PGnutellaSubgraph.append(0)


# Return the private hamiltonian cycle (regarding to the required graph)
def getPrivateHamiltonianCycle():
    return hamiltonianCycle2  # pathForP2PGnutellaSubgraph#pathForFacebookGraph#hamiltonianCycle3#hamiltonianCycle2#wrongPath#hamiltonianCycle