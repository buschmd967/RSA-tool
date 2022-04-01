import random
from utility import isPrime, pulverizer

def getPrimes(k):
    upper = pow(2, k+1)
    lower = (upper >> 2) + 1 #make sure it's odd
    
    p = random.randrange(lower, upper, 2)
    print("Finding p ", end="")
    while(not isPrime(p, k)):
        p = random.randrange(lower, upper, 2)
        while(p % 5 == 0):
            p = random.randrange(lower, upper, 2)
        print(".", end="", flush=True)
    q = random.randrange(lower, upper, 2)
    print("\nFinding q ", end="")
    while( q == p or not isPrime(q, k)):
        q = random.randrange(lower, upper, 2)
        while(q % 5 == 0):
            q = random.randrange(lower, upper, 2)
        print(".", end="", flush=True)
    print()
    return (p, q)

def generateED(phi):
    found = False
    e = random.randrange(1, phi, 2)
    d = -1
    while(not found):  
        p = pulverizer(phi, e)
        g = phi * p[0] + e * p[1]
        if(g == 1):
            found = True
            d = p[1] % phi
        else:
            e = random.randrange(1, phi, 2)
    return (e, d)

def generateKeys(k):
    p, q = getPrimes(k)
    n = p*q
    phi = (p-1) * (q-1)
    e, d = generateED(phi)

    with open("pubkeys", 'w') as f:
        f.write(f"n:{n}\ne:{e}")
    with open("privkeys", "w") as f:
        f.write(f"p:{p}\nq:{q}\nd:{d}")
    print("\"pubkeys\" and \"privkeys\" files have been generated.")