"""
Queens College
CSCI 355 - Internet and Web Technologies
Winter 2024
Assignment 9 - Error Detection and Correction
Shah Bhuiyan
Worked with Professor Teitelman + class
"""

from random import random, randint

def random_bits(n, p):
    return "".join(["1" if random() < p else "0" for _ in range(n)])

def change_bits(bits, m):
    list_bits = [*bits]
    for i in range(m):
        j = randint(0, len(bits) - 1)
        list_bits[j] = "1" if list_bits[j] == "0" else "0"
    return "".join(list_bits)

def ed_parity_1d(bits, even=True):
    parity_even = (sum([int(b) for b in bits]) % 2) == 0
    parity_bit = 0 if parity_even == even else 1
    print("ed_parity_1d: ", bits, even, parity_bit)
    return parity_bit

def ed_parity_2d(bits, width, even=True):
    n = len(bits)
    cols = width
    rows = n // cols
    rect1 = [bits[i * cols: (i + 1) * cols] for i in range(rows)]
    rect2 = ["".join(rect1[i][j] for i in range(len(rect1))) for j in range(cols)]
    parity_rows = [ed_parity_1d(s, even) for s in rect1]
    parity_cols = [ed_parity_1d(s, even) for s in rect2]
    print("ed_parity_2d: ", bits, even, parity_rows, parity_cols)
    return parity_rows, parity_cols


def ed_checksum(bits):
    n = len(bits)
    m = n//2
    r1, r2 = bits[:m], bits[m:]
    c = 0
    res = ""
    for j in range(m-1, -1, -1):
        b1, b2 = int(r1[j]), int(r2[j])
        s = b1 + b2 + c
        c = 1 if s > 1 else 0
        s = s - 2 * c
        res = str(s) + res
    comp = "".join(["0" if res[i] == "1" else "1" for i in range(len(res))])
    print("ed_checksum: ", bits, res, comp)
    return comp

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0: pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + [dividend[pick]]
        else:
            tmp = xor([0] * pick, tmp) + [dividend[pick]]
        pick += 1
    if tmp[0] == 1:
        tmp = xor(divisor, tmp)
    else:
        tmp = xor([0] * pick, tmp)
    checkword = tmp
    return checkword
def ed_crc(bits, key):
    data = [int(b) for b in bits]
    key = [int(k) for k in key]
    l_key = len(key)
    new_data = data + [0] * (l_key - 1)
    remainder = mod2div(new_data, key)
    codeword = data + remainder
    print("ed_crc: ", bits, key, "Remainder : ", remainder, "Encoded Data (Data + Remainder) : ", codeword)



def xor(a, b):
    return [a[i] == b[i] for i in range(1, len(b))]

def main():
    bits = "0111000110101011"
    ed_parity_1d(bits, True)
    print()

    bits2 = "10101" + "11110" + "01110"
    parity_rows, parity_cols = ed_parity_2d(bits2, 5, True)
    bits2c = change_bits(bits2, 1)


    parity_rows_c, parity_cols_c = ed_parity_2d(bits2c, 5, True)
    print()
    for i in range(len(parity_rows)):
        if parity_rows[i] != parity_rows_c[i]:
            print("mismatch found in row: ", i)
    for j in range(len(parity_rows)):
        if parity_rows[j] != parity_rows_c[j]:
            print("mismatch found in col: ", j)

    bits3 = "1110011001100110" + "1101010101010101"
    ed_checksum(bits3)
    print()

    bits4 = "100100"
    data = [int(b) for b in bits4]
    key = "1101"
    ed_crc(bits4, key)
    print()


if __name__ == "__main__":
    main()