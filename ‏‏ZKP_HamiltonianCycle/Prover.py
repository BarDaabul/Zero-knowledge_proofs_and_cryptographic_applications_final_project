# Submitted by:
# Bar Avraham Daabul
# Nadav Yosef Zada

# The Prover is the server and it communicates with the Verifier (the client)

import socket
import threading
import random
import numpy as np
import CommonGraph  # it contains the common graph
import PrivateHamiltonianCycle  # it contains the private hamiltonian cycle of the graph
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

    M = CommonGraph.getCommonGraph()  # the common graph
    hamiltonianCycle = PrivateHamiltonianCycle.getPrivateHamiltonianCycle()  # the private hamiltonian cycle

    # perform the first step of the prover
    print("Perform the first step of the prover")
    newM, permNodes, commitmentsArr, randValForDecArr = firstStepOfProver(conn, publicValues, M)
# $    totalCommunication = sys.getsizeof(str(commitmentsArr).encode(FORMAT))  # for the communication measurements
#    print("commitmentsArr:\n", commitmentsArr)
#    print("Prover's first step has finished\n")

# $    totalTimeMs = timeit.default_timer() - startCurrTimeMs  # current run time measurement
    chosenBitStr = conn.recv(NORM_BUF_SIZE).decode(FORMAT)  # wait until gets a bit from the verfier
# $    startCurrTimeMs = timeit.default_timer()  # The start time of the current section where the prover is running
# $    totalCommunication += sys.getsizeof(chosenBitStr.encode(FORMAT))  # for the communication measurements
    chosenBit = eval(chosenBitStr)
    print("The verifier chose the bit: ", chosenBit)

    # perform the second step of the prover
    print("Perform the second step of the prover:")
    strDec = secondStepOfProver(conn, newM, permNodes, randValForDecArr, chosenBit, hamiltonianCycle)
# $    totalCommunication += sys.getsizeof(strDec.encode(FORMAT))  # for the communication measurements
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


# Function that performs the prover's first step
# It performs a permutation of the nodes and get a new graph (adj matrix) and commits on the entries of the new graph
def firstStepOfProver(conn, publicValues, M):
    numOfNodes = len(M)
    currNodes = [i for i in range(numOfNodes)]  # the representation of the nodes

    newM, permNodes = PermForNodes(M, currNodes)  # perform a permutation of the nodes and get a new graph

    commitmentsArr, randValForDecArr = commitOnNewMatrix(newM, publicValues)  # get the commitments and the random values for the decs
    conn.send(str(commitmentsArr).encode(FORMAT))  # send the commitments to the verifier
    return newM, permNodes, commitmentsArr, randValForDecArr


# Function that gets a graph and an array of nodes
# It performs a permutation on the nodes and returns the new graph (adj matrix)
def PermForNodes(M, currNodes):
    numOfNodes = len(M)
    permNodes = np.random.permutation(currNodes)
    permNodes = [node for node in permNodes]  # changing the form of representation of the permutation

    newM = [[0 for i in range(numOfNodes)] for j in range(numOfNodes)]
    for i in range(numOfNodes):
        for j in range(numOfNodes):
            permI = permNodes[i]
            permJ = permNodes[j]
            newM[permI][permJ] = M[i][j]
    return newM, permNodes


# Function that gets a new graph (adj matrix) and public values
# It returns an array of commitments on the entries of the matrix and the random values that was used in the commitments
def commitOnNewMatrix(newM, publicValues):
    numOfNodes = len(newM)
    commitmentsArr = [[0]*2 for i in range(numOfNodes*numOfNodes)]  # it will contain the commitments for the entries of the matrix (each commitment has 2 components)
    randValForDecArr = [0]*numOfNodes*numOfNodes  # it will contain the random values that was used for the commitments

    q = publicValues[0]
    g = publicValues[1]
    y = publicValues[2]
    for k in range(numOfNodes*numOfNodes):  # commit on the value of each entry
        row = int(k / numOfNodes)
        col = int(k % numOfNodes)
        commitmentsArr[k], randValForDecArr[k] = ElGamalCommitmentScheme.commit(q, g, newM[row][col], y)
    return commitmentsArr, randValForDecArr


# Function that performs the prover's second step
# If chosenBit = 0, it sends to the verifier the permutation on the nodes and the decs of the new graph
# If chosenBit = 1, it sends to the verifier the decs of the hamiltonian cycle's edges in the new graph
def secondStepOfProver(conn, newM, permNodes, randValForDecArr, chosenBit, hamiltonianCycle):
    if(chosenBit == 0):
        print("Reveal the permutation and the commitments of the new graph's entries")
        return revealPermAndNewM(conn, newM, permNodes, randValForDecArr)  # sends to the verifier the permutation on the nodes and the decs of the new graph (newM)
    else:  # chosenBit == 1
        print("Reveal the commitments of the hamiltonian cycle's edges in the new graph")
        return revealNewHamiltonianCycle(conn, newM, permNodes, randValForDecArr, hamiltonianCycle)  # sends to the verifier the decs of the hamiltonian cycle's edges in the new graph (newM)


# A Function that sends to the verifier the permutation of the nodes and the decs of the new graph (newM)
def revealPermAndNewM(conn, newM, permNodes, randValForDecArr):
    strDec = str(permNodes)+"&"
    numOfNodes = len(newM)
    decArr = [[0]*2 for i in range(numOfNodes*numOfNodes)]  # it will contain the decs (value and random value) of each entry in the new graph (newM)
    for k in range(numOfNodes * numOfNodes):  # decommit of the values of each entry
        row = int(k / numOfNodes)
        col = int(k % numOfNodes)
        decArr[k] = [newM[row][col], randValForDecArr[k]]
    strDec += str(decArr)
    conn.send(strDec.encode(FORMAT))  # send the permutation of the nodes and the decs of the new graph (newM)
    return strDec


# A Function that sends to the verifier the decs of the hamiltonian cycle's edges in the new graph (newM)
def revealNewHamiltonianCycle(conn, newM, permNodes, randValForDecArr, hamiltonianCycle):
    numOfNodes = len(newM)
    permHamiltonianCycle = [permNodes[i] for i in hamiltonianCycle]
    strDec = str(permHamiltonianCycle) + "&"

    decArr = [[0] * 2 for i in range(len(permHamiltonianCycle)-1)]  # it will contain the decs (value and random value) of the entries in newM that represents the new hamiltonian cycle
    for k in range(len(decArr)):  # decommit of the required values
        row = permHamiltonianCycle[k]
        col = permHamiltonianCycle[k+1]
        decArr[k] = [newM[row][col], randValForDecArr[row * numOfNodes + col]]
    strDec += str(decArr)
    conn.send(strDec.encode(FORMAT))  # send the decs of the hamiltonian cycle's edges in the new graph (newM)
    return strDec


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding the current IP address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket
    start_server()
