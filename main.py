import copy
import numpy as np

def changeHexToDenary(table):
    hexMap = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
    for i in range(len(table)):
        entry = table[i]
        if (not (entry.isnumeric())):
            if entry in hexMap:
                table[i] = hexMap[entry]
            else:
                return -1
    return 1;

def inverseTable(table):
    inversedTable = np.empty(len(table), dtype=object)
    for i in range(len(table)):
        inversedTable[table[i]] = i
    return inversedTable

def createKeySchedules(key, boxSize, rounds, encrypt=True, inverse_permutation_table=None):
    portion = len(key) - rounds*boxSize
    keySchedules = [int(key[i:i+portion], 2) for i in range(0, (rounds+1)*boxSize, boxSize)]
    if (encrypt):
        return keySchedules
    else:
        if (inverse_permutation_table[0] == None): return -1
        return reverseAndPermutateKeys(keySchedules, inverse_permutation_table, portion)

def reverseAndPermutateKeys(keySchedules, inverse_permutation_table, portion):
    newKeySchedules = copy.deepcopy(keySchedules)
    for i in range(1, len(keySchedules)-1):
        newKeySchedules[i] = int(permutate(format(keySchedules[i],
                                                  f'0{portion}b'), inverse_permutation_table), 2)
    newKeySchedules.reverse()
    return newKeySchedules

def keyMix(input, keySchedules, round):
    return input ^ keySchedules[round-1]

def substitute(plaintext, substitution_table, boxSize):
    boxes = [int(plaintext[i:i+boxSize], 2)
             for i in range(0, len(plaintext), boxSize)] # Divide into boxes
    boxes = [substitution_table[box] for box in boxes] # Substitute
    boxes = "".join([format(box, f'0{boxSize}b') for box in boxes]) # Join boxes
    return boxes

def permutate(plaintext, permutation_table):
    plaintext = list(plaintext)
    ciphertext = np.empty(len(plaintext), dtype=object)
    for i in range(len(plaintext)):
        ciphertext[permutation_table[i]] = plaintext[i]
    return "".join(ciphertext)

def encrypt(plaintext, key, substitution_table, boxSize, permutation_table,
            rounds, encrypt=True):
    keySchedules = createKeySchedules(key, boxSize, rounds, encrypt, permutation_table)
    plaintext_length = len(plaintext)
    for i in range(1, rounds): # r=1 to Nr-1
        plaintext = format((keyMix(int(plaintext, 2), keySchedules, i)),
                           f'0{plaintext_length}b')
        plaintext = substitute(plaintext, substitution_table, boxSize)
        plaintext = permutate(plaintext, permutation_table)

    plaintext = format((keyMix(int(plaintext, 2), keySchedules, rounds)), #Nr
                       f'0{plaintext_length}b')
    plaintext = substitute(plaintext, substitution_table, boxSize)

    return format((keyMix(int(plaintext, 2), keySchedules, rounds+1)), #Nr+1
                  f'0{plaintext_length}b')

def setupProcess():
    file = open("tables.txt", "r")

    substitution_table = file.readline().strip().split(",")
    permutation_table = file.readline().strip().split(",")

    if (not changeHexToDenary(substitution_table)):
        print("Invalid format. Substitution table may only consist of"
              "hexadecimal letters.")
        return

    substitution_table = list(map(int, substitution_table))
    permutation_table = list(map(int, permutation_table))

    permutation_table = [x-1 for x in permutation_table]

    plaintext = '0100111010100001'
    key = '11100111011001111001000000111101'
    ciphertext = encrypt(plaintext, key, substitution_table, 4, permutation_table, 4)
    print(ciphertext)

    inverse_permutation_table = inverseTable(permutation_table)
    inverse_substitution_table = inverseTable(substitution_table)
    plaintext = encrypt(ciphertext, key, inverse_substitution_table, 4,
                        inverse_permutation_table, 4, False)
    print(plaintext)

# Main program
setupProcess()
