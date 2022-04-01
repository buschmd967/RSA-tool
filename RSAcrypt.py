#!/usr/bin/python3
from ast import Num
import sys
import random


from generators import *

help_message = "Encrypt/Decrypt : ./RSAcrypt.py [-e/-d] input_file.txt key_file.txt output_file.txt\nGenerate Keys   : ./RSAcrypt.py -g [k]"
pubkey_get_error_message = "Error: Could not get key from key file. Please make sure the public key file is formatted as:\nn:12345...\ne:12345..."
privkey_get_error_message = "Error: Could not get key from key file. Please make sure the private key file is formatted as:\np:12345...\nq:12345...\nd:12345..."

# ================= Key Retrevial =================

def getPubKeys(keys):
    k = keys.split("\n")
    if(len(k) != 2):
        print(pubkey_get_error_message)
        sys.exit()
    n = e = -1
    if(k[0][:2] == "n:" and k[0][2:].isnumeric()):
        n = int(k[0][2:])
    else:
        print(pubkey_get_error_message)
        sys.exit()
    if(k[1][:2] == "e:" and k[1][2:].isnumeric()):
        e = int(k[1][2:])
    else:
        print(pubkey_get_error_message)
        sys.exit()
    return (n, e)

def getPrivKeys(keys):
    k = keys.split("\n")
    if(len(k) != 3):
        print(privkey_get_error_message)
        sys.exit()
    p = q = d = -1
    if(k[0][:2] == "p:" and k[0][2:].isnumeric()):
        p = int(k[0][2:])
    else:
        print(privkey_get_error_message)
        sys.exit()
    
    if(k[1][:2] == "q:" and k[1][2:].isnumeric()):
        q = int(k[1][2:])
    else:
        print(privkey_get_error_message)
        sys.exit()
    
    if(k[2][:2] == "d:" and k[2][2:].isnumeric()):
        d = int(k[2][2:])
    else:
        print(privkey_get_error_message)
        sys.exit()
    return p, q, d

# ======== Encrypt and Decrypt =======     

def encrypt(plaintext, n, e):
    ciphertext = ""
    print("encrypting:\n")
    for c in plaintext:
        print(f"{chr(c)}", end="", flush=True)
        salt = random.randint(0, (2 ** 6) - 1)
        p = pow(c, e, n)
        echr = (pow(c, e, n) << 6 ) 
        echr = echr + salt
        ciphertext += str(echr) + "\n"
    print("\n")
    return ciphertext 

#Likely messed up the byte-related stuff here
def encryptFile(input_filename, key_filename, output_filename):
    with open(input_filename, 'rb') as ifile, open(key_filename, 'r') as kfile:
        plaintext = ifile.read()
        n, e = getPubKeys(kfile.read())
    ciphertext = encrypt(plaintext, n, e)
    with open(output_filename, "w") as f:
        f.write(ciphertext)
    print(f"File successfully encrypted as {output_filename}")


def decrypt(ciphertext, p, q, d):
    plaintext = b""
    print("decrypting:\n")
    for i in ciphertext.decode().split("\n"):
        i = i.replace("\n", "").replace("\r", "")
        if(i.isnumeric()):
            i = int(i)
            unsalted = i >> 6
            n = (p * q)
            intc = pow(unsalted, d, n)
            decc = chr(intc)
            plaintext += intc.to_bytes(2, 'big')
            print(chr(intc), end="", flush=True)
    print("\n")
    return plaintext

#Likely messed up the byte-related stuff here
def decryptFile(input_filename, key_filename, output_filename):
    with open(input_filename, "rb") as ifile, open(key_filename, 'r') as kfile:
        ciphertext = ifile.read()
        p, q, d = getPrivKeys(kfile.read())
    plaintext = decrypt(ciphertext, p, q, d)
    with open(output_filename, "wb") as f:
        f.write(plaintext)
    print(f"File sucessfully decrypted as {output_filename}")

# ===============================


def main():
    sys.setrecursionlimit(2000)

    if(len(sys.argv) != 5):
        if(len(sys.argv) == 2 or len(sys.argv) == 3):
            if(sys.argv[1] == "-g"):
                k = 1024
                if(len(sys.argv) == 3):
                    if(sys.argv[2].isnumeric()):
                        k = int(sys.argv[2])
                    else:
                        print(help_message)
                        sys.exit()
                generateKeys(k)
                sys.exit()
            else:
                print(help_message)
                sys.exit()

        else:
            print(help_message)
            sys.exit()
    else:
        _, mode, input_file, key_file, output_file = sys.argv
        if(mode == "-e"):
            encryptFile(input_file, key_file, output_file)
        elif(mode == "-d"):
            decryptFile(input_file, key_file, output_file)

if __name__ == "__main__":
    main()