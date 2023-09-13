# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada

# The Verifier is the client and it communicates with the Prover (the server)
import random
import socket
import CommonGraph  # it contains the common graph
import ElGamalCommitmentScheme  # it contains ElGamal commitment scheme
import timeit  # it is used for the running time measurements
import os  # it is used for the memory measurements
import psutil  # it is used for the memory measurements

# Define constants
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
NORM_BUF_SIZE = 1024  # The buffer size for the normal (not significantly heavy) data that is received in the communication
MAX_BUF_SIZE = 268435456  # the buffer size for the heavy data that is received in the communication

# Function that starts the client
def start_client():
    print("\nVerifier:\n")
    client_socket.connect((HOST, PORT))  # Connecting to server's socket
    isAccepted = client_socket.recv(NORM_BUF_SIZE).decode(FORMAT)  # Receiving data from the server after trying to connect
    if isAccepted == "Error: The prover is already connected to a verifier":
        print(isAccepted)
        return

    # Receiving public values for using the commitment scheme from the server
    publicValuesStr = client_socket.recv(NORM_BUF_SIZE).decode(FORMAT)
    publicValues = eval(publicValuesStr)
#    print("publicValues:", publicValues)
    client_socket.send("Public values were received".encode(FORMAT))  # Sending acknowledgment to the server

    # The measurements are tested from the beginning of the protocol (when the participants get the protocol's inputs):
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the verifier is running
    # for the total memory consumption measurements
# $    process = psutil.Process(os.getpid())  # get the current process
# $    memory_start = process.memory_info().rss / (1024 * 1024)  # get the memory usage (MB) in the beginning

    M = CommonGraph.getCommonGraph()  # the common graph

# $    totalTimeMs = timeit.default_timer() - startCurrTimeMs  # current run time measurement

    # Receiving an array of commitments on the entries of the new graph (newM)
    commitmentsArrStr = client_socket.recv(MAX_BUF_SIZE).decode(FORMAT)
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the verifier is running
    commitmentsArr = convertStringToMatrix(commitmentsArrStr)
#    print("commitmentsArr\n", commitmentsArr)

    print("Perform the first step of the verifier")
    chosenBit = firstStepOfVerifier(client_socket)  # choose a random bit and send it to prover
#    print("Verifier's first step has finished\n")

# $    totalTimeMs += (timeit.default_timer() - startCurrTimeMs)  # current run time measurement
    strDec = client_socket.recv(MAX_BUF_SIZE).decode(FORMAT)  # wait until gets dec from the prover (after prover's second step)
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the verifier is running
    dec = [strDec.split("&")[0], strDec.split("&")[1]]
    dec1 = eval(dec[0])
    dec2 = convertStringToMatrix(dec[1])
    # if b=0, dec=[permNodes, decArr (decs for all the entries in newM)].
    # if b=1, dec=[permHamiltonianCycle, decArr (decs of the entries that represent the new hamiltonian cycle)].
    dec = [dec1, dec2]

    print("Perform the second step of the verifier:")
    hasHamiltonianCycle = secondStepOfVerifier(client_socket, chosenBit, publicValues, dec, commitmentsArr, M)
    if hasHamiltonianCycle:
        print("\nAccept the claim - the graph has a hamiltonian cycle!")
    else:
        print("\nReject the claim - the graph doesn't have a hamiltonian cycle!")
#    print("\nVerifier's second step has finished\n")

    # The protocol finished its operation. From here, there are some measurement results:
# $    print("\nmeasurement result:")
    # total run time measurement
# $    totalTimeMs += (timeit.default_timer() - startCurrTimeMs)  # current run time measurement
# $    print(f"The execution time of the verifier: {totalTimeMs:.3f} sec")

    # total memory consumption measurement:
# $    memory_end = process.memory_info().rss / (1024 * 1024)  # get the memory usage (MB) in the end
# $    memory_usage = memory_end - memory_start
# $    print(f"The memory usage of the verifier: {memory_usage:.3f} MB")

    return


# Function that convert string to an array (matrix form)
def convertStringToMatrix(matrix):
    newMatrix = matrix.replace("\n ", ", ")
    newMatrix = newMatrix.replace(" ", ", ")
    newMatrix = newMatrix.replace(",, ", ", ")
    return eval(newMatrix)


# Function that performs the verifier's first step (choose a random bit and send it to the prover)
def firstStepOfVerifier(client_socket):
    chosenBit = random.randint(0, 1)  # choose random bit (0 or 1)
    print("The chosen bit: ", chosenBit)
    client_socket.send(str(chosenBit).encode(FORMAT))
    return chosenBit


# Function that performs the verifier's second step
def secondStepOfVerifier(client_socket, chosenBit, publicValues, dec, commitmentsArr, M):
    if chosenBit == 0:
        print("Check if the decommits are valid and if the new graph is isomorphic to the original graph")
        hasHamiltonianCycle = checkDecAndIsomorphicGraphs(publicValues, dec, commitmentsArr, M)
    else:  # chosenBit == 1
        print("Check if the decommits are valid and if the given path is a hamiltonian cycle")
        hasHamiltonianCycle = checkDecAndHamiltonianCycle(publicValues, dec, commitmentsArr, len(M))

    if (hasHamiltonianCycle):
        client_socket.send(str("Accept").encode(FORMAT))
    else:
        client_socket.send(str("Reject").encode(FORMAT))

    return hasHamiltonianCycle


# A Function that check the decs of the new graph and check that the new graph is isomorphic to the original graph
def checkDecAndIsomorphicGraphs(publicValues, dec, commitmentsArr, M):
    # dec=[permNodes, decArr (decs for all the entries in newM)].
    permNodes = dec[0]
    decArr = dec[1]  # decs for all the entries in newM

    # the public values
    q = publicValues[0]
    g = publicValues[1]
    y = publicValues[2]

    numOfNodes = len(M)
    newM = [[0 for i in range(numOfNodes)] for j in range(numOfNodes)]
    for k in range(numOfNodes * numOfNodes):  # numOfNodes * numOfNodes = len(decArr)
        isValidDec = ElGamalCommitmentScheme.verify(q, g, y, decArr[k], commitmentsArr[k])
        if(not isValidDec):
            return False
        currValEntry = decArr[k][0]
        if(currValEntry == 1):  # Otherwise the value is initialized to 0
            row = int(k / numOfNodes)
            col = int(k % numOfNodes)
            newM[row][col] = currValEntry

    # create the mapping for the nodes
    mappingNodes = {}
    for i in range(len(permNodes)):
        mappingNodes[i] = permNodes[i]
    return areIsomorphicGraphs(M, newM, mappingNodes)


# A Function that get an original graph, a new graph and a mapping of the permutation of the nodes
# It returns True if the graphs are isomorphic by the given mapping, and False otherwise
def areIsomorphicGraphs(M, newM, mappingNodes):
    if len(M) != len(newM):  # check if the number of nodes is the same
        return False
    # check that every entry in the original graph has the same value as the corresponding entry in the new graph using the permutation
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != newM[mappingNodes.get(i)][mappingNodes.get(j)]:
                return False
    return True


# A Function that check the decs of the new cycle and check that the new cycle is hamiltonian
def checkDecAndHamiltonianCycle(publicValues, dec, commitmentsArr, numOfNodes):
    # dec=[permHamiltonianCycle, decArr (decs of the entries that represent the new hamiltonian cycle)].
    permHamiltonianCycle = dec[0]
    decArr = dec[1]  # decs of the entries that represent the new hamiltonian cycle

    # the public values
    q = publicValues[0]
    g = publicValues[1]
    y = publicValues[2]

    for k in range(len(permHamiltonianCycle)-1):  # len(permHamiltonianCycle)-1 = len(decArr)
        row = permHamiltonianCycle[k]
        col = permHamiltonianCycle[k+1]

        isValidDec = ElGamalCommitmentScheme.verify(q, g, y, decArr[k], commitmentsArr[row * numOfNodes + col])
        currValEntry = decArr[k][0]
        if (not isValidDec) or (currValEntry != 1):  # if the dec is not valid or there is no edge in the current entry, return False
            return False
    return isHamiltonianCycle(permHamiltonianCycle, numOfNodes)


# A Function that get a path in a graph, and the num of nodes in the graph.
# It returns True if the path is hamiltonian cycle in the graph, and False otherwise
def isHamiltonianCycle(permHamiltonianCycle, numOfNodes):
    # checking if permHamiltonianCycle is a cycle (starts and ends in same node)
    if (permHamiltonianCycle[0] != permHamiltonianCycle[len(permHamiltonianCycle)-1]):
        return False

    startNode = permHamiltonianCycle[0]

    # count the number of appearance for each node
    countNodesAppearance = [0]*numOfNodes
    for node in permHamiltonianCycle:
        countNodesAppearance[node] += 1

    if (countNodesAppearance[startNode] != 2):  # if the start node doesn't appear exactly twice, return False
        return False
    for i in range(numOfNodes):
        if (i != startNode and countNodesAppearance[i] != 1):  # if the current node is not the start node and it doesn't appear exactly one time, return False
            return False
    return True


# Main
if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())  # finding the current IP address
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Client socket
    start_client()
    client_socket.close()  # Closing client's connection with server (<=> closing socket)
    print("\nThe interaction with the prover has finished")
