"""
Queens College
CSCI 355 - Internet and Web Technologies
Winter 2024
Assignment 7 - Network Addressing and Routing
Shah Bhuiyan
Worked with class and professor teitelman
"""
import binascii
from subprocess import check_output
# [1] Write a function execute_command(cmd) to execute a windows shell command ("cmd").
def exec_cmd(cmd):
    return check_output(cmd, shell=True)





"""
[2] Define a function get_routing_table by using the function from the previous step to
run "route print" and then parsing the output into a table (2-D list).
"""
def get_routing_table(routing_data):
    s = routing_data.decode()
    s = s[s.find("Destination"): s.find("Internet6") - 1].strip()
    lines = s.split("\n")
    print(s)
    data = [[get(line, 0, 17), get(line, 18, 37), get(line, 38, 44), get(line, 45, 62), get(line, 63, 70)] for line in lines]
    for row in data:
        print(row)
    return data

def get(s, i, j):
    return s[i:j+1].strip()

"""
[4] Define a function validate_address() to validate the address in two ways:
Call your own function to check that the entered IP address is valid, that is, it consists of four decimal numbers, each between 0 and 255, and separated by dots (periods). 
Call code from socket package to validate it. See https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python   """

def validate_address(ip_address):
    if ip_address.count(".") != 3:
        return f"Invalid IP Address: {ip_address} requires 4 octets."
    else:
        octets = ip_address.split(".")
        for octet in octets:
            if not octet.isnumeric():
                return f"IP address: {octet} is not numeric"
            else:
                n = int(octet)
                if n < 0 or n > 255:
                    return f"{octet} must have octet between 0 and 255"

    return ""

"""
[5] Define a function get_binary_address() to  find the binary equivalent of an IP address in 
dotted decimal notation and use it on the inputted IP address. 
"""

def binary_address(ip_address):
    octet = ip_address.split('.')
    binary = "".join([bin(int(octet))[2:].zfill(8) for octet in octet])
    return binary

def main():
    routing_data = exec_cmd("route print")
    table = get_routing_table(routing_data)
    destinations = []
    for i in range(1, len(table[1:])):
        row = table[i]
        addr = row[0]
        idx = addr.find("/")
        if idx > 0:
            addr = addr[0:idx]
        msg = validate_address(addr)
        if len(msg) == 0:
            destinations.append([i, addr, binary_address(addr)])
    while True:
        ip_address = input("Enter IP Address: ")
        msg = validate_address(ip_address)
        if len(msg) > 0:
            print(msg)
        else:
            binary = binary_address(ip_address)
            most_bits_matched = 0
            best_row_matched = -1
            for dest in destinations:
                bits_match = 0
                for i in range(len(binary)):
                    dest_binary = dest[2]
                    if binary[i] == dest_binary[i]:
                        bits_match += 1
                    else:
                        break
                if bits_match > most_bits_matched:
                    most_bits_matched = bits_match
                    best_row_matched = dest
            table_row = table[best_row_matched[0]]
            print("Best Matched: ", most_bits_matched, best_row_matched, table_row[0], "Gateway: ", table_row[1])



if __name__ == "__main__":
    main()


