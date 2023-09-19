# Zero-knowledge_proofs_and_cryptographic_applications_final_project
This repository contains the final project for a bachelor's degree in computer engineering on the topic of zero-knowledge proofs and cryptographic applications.

In the project, there are implementation of two ZKP protocols - ZKP for graph 3 coloring (G3C) and ZKP for hamiltonian cycle (HC). In addition, several experiments are carried out in order to test the efficiency of the protocols and compare them.

In the folder "ZKP_Graph3Coloring", there are python files of the implementation of the ZKP for G3C. Moreover, in this folder there is a folder "data" which contains the data of the graphs that was used for the experiments.

In the folder "‏‏ZKP_HamiltonianCycle", there are python files of the implementation of the ZKP for HC. In this folder there is also a folder "data" which contains the data of the graphs that was used for the experiments.

The results of the experiments are in excel files that in the folder "Experiments' results".

The repository also contains the final presentation, the project book, and the poster.

# Usage

In order to run the codes of the project, follow these steps:

Clone the repository to your local machine:

git clone https://github.com/BarDaabul/Zero-knowledge_proofs_and_cryptographic_applications_final_project.git

## For the ZKP for G3C, run the code in the following way:

Open the code files that in the folder "ZKP_Graph3Coloring", in a work environment that can run Python files

In the file CommonGraph.py, return the required graph (the common input of the prover and the verifier) in getCommonGraph function.

In the file PrivateColoring.py, return the required coloring (the private input of the prover) in getPrivateColoring function.

Run Prover.py, and then run Verifier.py (After the running, the output of the protocol will be printed).

## For the ZKP for HC, run the code in the following way:

Open the code files that in the folder "‏‏ZKP_HamiltonianCycle", in a work environment that can run Python files

In the file CommonGraph.py, return the required graph (the common input of the prover and the verifier) in getCommonGraph function.

In the file PrivateHamiltonianCycle.py, return the required path (the private input of the prover) in getPrivateHamiltonianCycle function.

Run Prover.py, and then run Verifier.py (After the running, the output of the protocol will be printed).

# Acknowledgements
Bar Avraham Daabul, Nadav Yosef Zada.
