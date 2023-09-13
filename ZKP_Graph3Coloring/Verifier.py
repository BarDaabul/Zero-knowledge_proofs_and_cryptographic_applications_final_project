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
MAX_BUF_SIZE = 4194304  # the buffer size for the heavy data that is received in the communication


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

    G = CommonGraph.getCommonGraph()  # the common graph

# $    totalTimeMs = timeit.default_timer() - startCurrTimeMs  # current run time measurement

    # Receiving an array of commitments on the colors of each vertex from the server
    commitmentsArrStr = client_socket.recv(MAX_BUF_SIZE).decode(FORMAT)
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the verifier is running
    commitmentsArr = convertStringToMatrix(commitmentsArrStr)
#    print("commitmentsArr\n", commitmentsArr)

    print("Perform the first step of the verifier")
    chosenEdge = firstStepOfVerifier(client_socket, G)  # choose random edge and send it to prover, chosenEdge=[u, v]
#    print("Verifier's first step has finished\n")

# $    totalTimeMs += (timeit.default_timer() - startCurrTimeMs)  # current run time measurement
    edgeDecStr = client_socket.recv(NORM_BUF_SIZE).decode(FORMAT)  # wait until gets dec1 and dec2 from the prover (after prover's second step)
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the verifier is running
    edgeDec = eval(edgeDecStr)
    print("Perform the second step of the verifier")
    is3Coloring = secondStepOfVerifier(client_socket, chosenEdge, publicValues, edgeDec, commitmentsArr)
    if(is3Coloring):
        print("\nAccept the claim - the graph is a 3-coloring!")
    else:
        print("\nReject the claim - the graph is not a 3-coloring!")
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


# Function that performs the verifier's first step (choose a random edge from the graph and send it to the prover)
def firstStepOfVerifier(client_socket, G):
    # If the matrix length is nxn (the adjacency matrix is square), so the vertices are numbered from 0 to n-1.
    # We will choose random edge from the graph.
    chosenEdge = chooseRandomEdge(G)  # the chosen edge
    print("The chosen edge: ", chosenEdge)
    client_socket.send(str(chosenEdge).encode(FORMAT))
    return chosenEdge


# Function that get a graph and return a random edge from the graph
def chooseRandomEdge(G):
    edges = []
    # Take all the edges from the adjacency matrix to a list of edges
    for u in range(len(G)):
        for v in range(u+1, len(G)):
            if G[u][v] == 1:
                edges.append([u, v])

    chosenEdge = random.choice(edges)  # choose a random edge
    return chosenEdge


# Function that performs the verifier's second step (check the opening of the commitments and output accept or reject)
def secondStepOfVerifier(client_socket, chosenEdge, publicValues, edgeDec, commitmentsArr):
    dec1 = edgeDec[0]  # the dec for the first vertex
    dec2 = edgeDec[1]  # the dec for the second vertex
    colorVal1 = dec1[0]  # the color (the value) for the first vertex
    colorVal2 = dec2[0]  # the color (the value) for the second vertex

    # the public values
    q = publicValues[0]
    g = publicValues[1]
    y = publicValues[2]

    v1 = chosenEdge[0]  # the index of the first vertex
    v2 = chosenEdge[1]  # the index of the second vertex

# if the opening of the commitments is correct and the colors of the vertices are different, is3Coloring = true
# else (one of the tests gives false), is3Coloring = false
    is3Coloring = ElGamalCommitmentScheme.verify(q, g, y, dec1, commitmentsArr[v1]) and ElGamalCommitmentScheme.verify(q, g, y, dec2, commitmentsArr[v2]) and (colorVal1 != colorVal2)
    if(is3Coloring):
        client_socket.send(str("Accept").encode(FORMAT))
    else:
        client_socket.send(str("Reject").encode(FORMAT))
    return is3Coloring


# Main
if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())  # finding the current IP address
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Client socket
    start_client()
    client_socket.close()  # Closing client's connection with server (<=> closing socket)
    print("\nThe interaction with the prover has finished")
