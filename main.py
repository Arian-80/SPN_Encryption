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

def createKeySchedules(key, boxSize, rounds):
    portion = len(key) - rounds*boxSize
    return [int(key[i:i+portion], 2) for i in range(0, (rounds+1)*boxSize, boxSize)]

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

def encrypt(plaintext, key, substitution_table, boxSize, permutation_table, rounds):
    keySchedules = createKeySchedules(key, boxSize, rounds)

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

    boxSize = 4
    keySchedules = createKeySchedules('11100111011001111001000000111101', boxSize, 4)

    plaintext = '0100111010100001'
    plaintext_length = len(plaintext)
    plaintext = format((keyMix(int(plaintext, 2), keySchedules, 1)), f'0{plaintext_length}b')

    plaintext = substitute(plaintext, substitution_table, boxSize)
    plaintext = permutate(plaintext, permutation_table)


# Main program
setupProcess()
