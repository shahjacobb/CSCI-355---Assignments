"""
Queens College
CSCI 355 - Internet and Web Technologies
Winter 2024
Assignment 10 - Data Compression
Shah Bhuiyan
Worked with the class and Prof Teitelman
"""


import heapq
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()


def binary(text):
    return "".join([bin(ord(char))[2:].zfill(8) for char in text])


# [1] Define functions that implement each of the four data compression algorithms:

def dc_run_length_encoding_v1(text):
    n = len(text)
    i = 0
    result = ""
    while i < n - 1:
        count = 1
        while i < n - 1 and text[i] == text[i + 1]:
            count += 1
            i += 1
        i += 1
        result += text[i - 1] + " " + str(count) + ","
    return result


# V2 of run length encoding
# see slide 8.9 of other slides
def dc_run_length_encoding_v2(binary_text):
    if sum([1 if char not in "01" else 0 for char in binary_text]) > 0:
        raise ValueError("Input must be binary")
    count = 0
    result = ""
    i = 0
    while i < len(binary_text):
        if binary_text[i] == "0":
            count += 1
        else:  # binary_text[i] == "1"
            result += str(count) + ","
            count = 0
        i += 1
    result += str(count)
    return result


class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''
    def __lt__(self, nxt):
        return self.freq < nxt.freq


def get_codes(codes, node, val=''):
    newVal = val + str(node.huff)
    if node.left:
        get_codes(codes, node.left, newVal)
    if node.right:
        get_codes(codes, node.right, newVal)
    if not node.left and not node.right:
        codes[node.symbol] = newVal


def dc_huffman_coding(chars, freqs):
    nodes = []
    for x in range(len(chars)):
        heapq.heappush(nodes, node(freqs[x], chars[x]))
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        left.huff = 0
        right.huff = 1
        newNode = node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        heapq.heappush(nodes, newNode)
    codes = {}
    get_codes(codes, nodes[0])
    return codes


def dc_lempel_ziv_welch(alphabet, text):
    table = {}
    i = 0
    while i < len(alphabet):
        table[alphabet[i]] = i
        i += 1
    j = 0
    p = text[j]
    result = ''
    while j < len(text) - 1:
        j += 1
        c = text[j]
        if p + c in table:
            p = p + c
        else:
            result += str(table[p]) + ","
            table[p + c] = i
            i += 1
            p = c
    result += str(table[p])
    return result


def compute_cum_freqs(freqs):
    cum_freqs = [0]
    cum_freq = 0
    for i, freq in enumerate(freqs):
        if i == len(freqs) - 1:
            break
        cum_freq += freq
        cum_freqs.append(cum_freq)
    return cum_freqs


def interval_to_binary(interval_start, interval_finish):
    bin_str = ""
    prob = 0
    index = 0
    while prob < interval_start:
        index += 1
        power = 1/(2**index)
        if prob + power <= interval_finish:
            bin_str += "1"
            prob += power
        else:
            bin_str += "0"
    return bin_str


def dc_arithmetic_coding(message, chars, freqs):
    cum_freqs = compute_cum_freqs(freqs)
    interval0 = 0
    interval1 = 1
    for char in message:
        idx = chars.index(char)
        freq = freqs[idx]
        cum_freq = cum_freqs[idx]
        interval_size = interval1 - interval0
        interval0 += interval_size * cum_freq
        interval1 = interval0 + freq * interval_size
    return interval_to_binary(interval0, interval1)


def main():
    text = read_file("Assignment8d.txt")
    print("RLE v1 MLK Speech:", dc_run_length_encoding_v1(text))
    text_binary = binary(text)
    print("RLE v1 Binary of MLK Speech:", dc_run_length_encoding_v1(text_binary))

    text_binary = "0" * 12 + "1" + "0" * 3 + "11" + "0" * 8
    print("RLE v2 Binary of examples from slides:", dc_run_length_encoding_v2(text_binary))

    text = 'BAABABBBAABBBBAA'
    alphabet = ['A', 'B']
    print("LZW examples from slides:", dc_lempel_ziv_welch(alphabet, text))

    alphabet = ['A', 'B', 'C', 'D', 'E']
    freqs = [20, 10, 10, 30, 30]
    print("Huffman coding from slides:", dc_huffman_coding(alphabet, freqs))

    # see figure 8.7 on slide 8.2
    text = "BBAB*"
    alphabet = ["A", "B", "*"]
    freqs = [.4, .5, .1]
    print("Arithmetic coding from slides:", dc_arithmetic_coding(text, alphabet, freqs))


if __name__ == '__main__':
    main()