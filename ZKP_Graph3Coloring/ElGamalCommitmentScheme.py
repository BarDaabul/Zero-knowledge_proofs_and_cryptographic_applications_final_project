#  implementation of ElGamalCommitmentScheme which providing a computationally hiding and statistically binding
#  Submitted by:
#  Bar Avraham Daabul
#  Nadav Yosef Zada

import random


# Calculate the gcd of a and b
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# Generate the secret key (sk) and the public key (pk)
def generateKeys(q, g):
    secretKey = random.randint(pow(2, 224), q)
    while gcd(q, secretKey) != 1:
        secretKey = random.randint(pow(2, 224), q)  # secret key (sk)

    publickKey = modPow(g, secretKey, q)  # public key (pk) [g^key % q]
    return secretKey, publickKey


# Calculate modular exponentiation
def modPow(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c


# Commit on value
def commit(q, g, value, y):
    r = random.randint(1, q-2)  # random value
    c1 = modPow(g, r, q)  # c1 = g^r % q
    c2 = (value * modPow(y, r, q)) % q  # c2 = [value * (y^r % q)] % q
    C = [c1, c2]  # the commitment is C = [c1,c2]
    return C, r


# Verify on value (dec = [value, r])
def verify(q, g, y, dec, commitFromCommitStep):
    value = dec[0]
    r = dec[1]

    checkC1 = modPow(g, r, q)  # checkC1 = g^r % q
    checkC2 = (value * modPow(y, r, q)) % q  # checkC2 = [value * (y^r % q)] % q

    if(checkC1 != commitFromCommitStep[0]) or (checkC2 != commitFromCommitStep[1]):
        return False  # the reveal for the commit is not corresponding to the given values
    return True  # the reveal for the commit is correct
