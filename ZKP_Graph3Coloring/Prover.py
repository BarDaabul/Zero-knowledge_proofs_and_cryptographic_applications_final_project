# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada

# The Prover is the server and it communicates with the Verifier (the client)

import socket
import threading
import random
import numpy as np
import CommonGraph  # it contains the common graph
import PrivateColoring  # it contains the private coloring of the graph
import ElGamalCommitmentScheme  # it contains ElGamal commitment scheme
import timeit  # it is used for the running time measurements
import os  # it is used for the memory measurements
import psutil  # it is used for the memory measurements
import sys  # it is used for the communication measurements

# Define constants
HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 60000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
NORM_BUF_SIZE = 1024  # The buffer size for the normal (not significantly heavy) data that is received in the communication


# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple
    server_socket.listen(1)  # Server is open for connection to one client

    while True:
        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)

        if threading.activeCount() - 1 == 1:  # Check if the maximum number of clients has reached
            connection.send("Error: The prover is already connected to a verifier".encode(FORMAT))
            connection.close()
            continue

        if threading.activeCount() - 1 < 1:  # Check if the maximum number of clients hasn't reached
            connection.send("Accepted".encode(FORMAT))
            thread = threading.Thread(target=handle_client, args=(connection, address))  # Creating new Thread object.
            thread.start()  # Starting the new thread (<=> handling new client)


# Function that handles a single client connection
# It performs the steps of the prover in the protocol
def handle_client(conn, addr):
    print("\nProver:\n")
    # values for using the ElGamal commitment scheme
    q = random.randint(pow(2, 224), pow(2, 256))  # order of the cyclic group
    g = random.randint(2, q)  # generator of the group
    key, y = ElGamalCommitmentScheme.generateKeys(q, g)  # key = secret key (sk), y = public key (pk) [y=g^key % q]

    publicValues = [q, g, y]  # public values for using the ElGamal commitment scheme
#    print("publicValues:", publicValues)
    conn.send(str(publicValues).encode(FORMAT))
    conn.recv(NORM_BUF_SIZE).decode(FORMAT)  # wait until gets ack ("Public values were received") from the verfier

    # The measurements are tested from the beginning of the protocol (when the participants get the protocol's inputs):
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the prover is running
    # for the total memory consumption measurements
# $    process = psutil.Process(os.getpid())  # get the current process
# $    memory_start = process.memory_info().rss / (1024 * 1024)  # get the memory usage (MB) in the beginning

    G = CommonGraph.getCommonGraph()  # the common graph
    coloring = PrivateColoring.getPrivateColoring()  # the private 3-coloring

    # perform the first step of the prover
    print("Perform the first step of the prover")
    permColoring, commitmentsArr, randValForDecArr = firstStepOfProver(conn, publicValues, coloring)
# $    totalCommunication = sys.getsizeof(str(commitmentsArr).encode(FORMAT))  # for the communication measurements
#    print("commitmentsArr:\n", commitmentsArr)
#    print("Prover's first step has finished\n")

# $    totalTimeMs = timeit.default_timer() - startCurrTimeMs  # current run time measurement
    chosenEdgeStr = conn.recv(NORM_BUF_SIZE).decode(FORMAT)  # wait until gets an edge from the verfier
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the prover is running
# $    totalCommunication += sys.getsizeof(chosenEdgeStr.encode(FORMAT))  # for the communication measurements
    chosenEdge = eval(chosenEdgeStr)
    print("The verifier chose the edge: ", chosenEdge)

    # perform the second step of the prover
    print("Perform the second step of the prover")
    edgeDec = secondStepOfProver(conn, permColoring, randValForDecArr, chosenEdge)
# $    totalCommunication += sys.getsizeof(str(edgeDec).encode(FORMAT))  # for the communication measurements
#    print("Prover's second step has finished\n")

# $    totalTimeMs += (timeit.default_timer() - startCurrTimeMs)  # current run time measurement
    resultFromVerifier = conn.recv(NORM_BUF_SIZE).decode(FORMAT)  # wait until gets the result (accept/reject) from the verfier
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the prover is running
# $    totalCommunication += sys.getsizeof(resultFromVerifier.encode(FORMAT))  # for the communication measurements

    if resultFromVerifier == "Accept":
        print("\nThe verifier accepted the claim!")
    else:
        print("\nThe verifier rejected the claim!")


    # The protocol finished its operation. From here, there are some measurement results:
# $    print("\nmeasurement result:")
    # total run time measurement
# $    totalTimeMs += (timeit.default_timer() - startCurrTimeMs)  # current run time measurement
# $    print(f"The execution time of the prover: {totalTimeMs:.3f} sec")

    # total memory consumption measurement:
# $    memory_end = process.memory_info().rss / (1024 * 1024)  # get the memory usage (MB) in the end
# $    memory_usage = memory_end - memory_start
# $    print(f"The memory usage of the prover: {memory_usage:.3f} MB")

    # total communication measurement:
# $    print(f"The amount of data used for communication of both sides (prover and verifier): {totalCommunication / (1024 * 1024):.3f} MB")

    conn.close()  # close the connection with the verifier


# Function that performs the prover's first step (perform a permutation of the colors and commits on the new colors)
def firstStepOfProver(conn, publicValues, coloring):
    colors = [1, 2, 3]  # the representation of the colors
    permColoring = PermForColoring(colors, coloring)  # perform a permutation of the colors
    commitmentsArr, randValForDecArr = commitOnColoring(permColoring, publicValues)  # get the commitments and the random values for the decommitments
    conn.send(str(commitmentsArr).encode(FORMAT))  # send the commitments to the verifier
    return permColoring, commitmentsArr, randValForDecArr


# Function that gets an array of 3-colors and an array of coloring.
# It performs permutation on the colors and returns an array of the new coloring
def PermForColoring(colors, coloring):
    premColors = np.random.permutation(colors)
##    while premColors[0] == 1 and premColors[1] == 2 and premColors[2] == 3:  # check if premColors is the same as colors
##        premColors = np.random.permutation(colors)

    permColoring = np.copy(coloring)
    for i in range(len(permColoring)):
        if coloring[i] == 1:
            permColoring[i] = premColors[0]
        if coloring[i] == 2:
            permColoring[i] = premColors[1]
        if coloring[i] == 3:
            permColoring[i] = premColors[2]
    return permColoring


# Function that gets a coloring of the vertices and public values
# It returns an array of commitments on the coloring and the random values that was used in the commitments.
def commitOnColoring(permColoring, publicValues):
    commitmentsArr = [[0]*2 for i in range(len(permColoring))]  # it will contain the commitments for the color of each vertex (each commitment has 2 components)
    randValForDecArr = [0]*len(permColoring)  # it will contain the random values that was used for the commitments

    q = publicValues[0]
    g = publicValues[1]
    y = publicValues[2]
    for i in range(len(permColoring)):  # commit on the colors of each vertex
        commitmentsArr[i], randValForDecArr[i] = ElGamalCommitmentScheme.commit(q, g, permColoring[i], y)
    return commitmentsArr, randValForDecArr


# Function that performs the prover's second step (send the dec for the two vertices that was chosen by the verifier)
def secondStepOfProver(conn, permColoring, randValForDecArr, chosenEdge):
    v1 = chosenEdge[0]  # the first node of the chosen edge
    v2 = chosenEdge[1]  # the second node of the chosen edge
    colorVal1 = permColoring[v1]  # the color (the value) of the first node
    colorVal2 = permColoring[v2]  # the color (the value) of the second node
    randomVal1 = randValForDecArr[v1]  # the random value of the commitment on the first node
    randomVal2 = randValForDecArr[v2]  # the random value of the commitment on the second node
    dec1 = [colorVal1, randomVal1]
    dec2 = [colorVal2, randomVal2]
    edgeDec = [dec1, dec2]  # the decs of the chosen edge
    conn.send(str(edgeDec).encode(FORMAT))  # send the decs of the chosen edge to the verifier
    return edgeDec


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding the current IP address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket
    start_server()
