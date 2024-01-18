"""
Queens College
CSCI 355 - Internet and Web Technologies
Winter 2024
Assignment1.py
Shah Bhuiyan
Worked with the class
"""

import sys
import socket

# [1] Define a function get_host_info() to determine your computer’s IP address.
def get_host_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("Your Computer Name:", hostname)
    print("Your Computer IP Address:", ip_address)
    bin_addr = binary_address(ip_address)
    print("The binary address is ", bin_addr)
    cls = get_class(bin_addr)
    print("The class is", cls)
    port_num_ex = 80
    port_type_ex = port_type(port_num_ex)
    print("The port type of ", port_num_ex, "is ", port_type_ex)

# [2] Define a function binary_address() to convert your IP Address from “dotted decimal notation” to a 32-bit binary string.
def binary_address(ip_address):
    octet = ip_address.split('.')
    binary = "".join([bin(int(octet))[2:].zfill(8) for octet in octet])
    return binary

# [3] Write a function to determine if the address is Class A, B, C, D or E by examining the first few bits of the 32-bit string.
def get_class(binary_address):
    if binary_address[0:1] == "0":
        cls = "A"
    elif binary_address[0:2] == "10":
        cls = "B"
    elif binary_address[0:3] == "110":
        cls = "C"
    elif binary_address[0:4] == "1110":
        cls = "D"
    elif binary_address[0:5] == "1111":
        cls = "E"
    return cls

"""
[4] Define a function port_type(port) to determine the type of port number. The options are:

0-1023: Well-Known
1024-49151: Registered
49152-65535: Dynamic/Private 
"""
def port_type(port):
    pt = "?"
    if 0 <= port < 1024:
        pt = "Well Known"
    elif 1024 <= port < 49152:
        pt = "Registered"
    elif 49152 <= port < 65536:
        pt = "Dynamic/Private"
    return pt


# [5] Write a function to connect to the Google server https://www.geeksforgeeks.org/socket-programming-python/ #
# An example script to connect to Google using socket programming in Python

def connect_to_server(domain_name, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))
    try:
        host_ip = socket.gethostbyname(domain_name)
    except socket.gaierror:
        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()
    # connecting to the server
    s.connect((host_ip, port))
    print("the socket has successfully connected to", domain_name, "on port", port)
    s.close()


# [7] Write a programs Assignment2Client.py that will talk to that server

def connect_to_server_v2(hostname, port):
    # Create a socket object
    s = socket.socket()
    # Gets the IP address
    ip_addr = socket.gethostbyname(hostname)
    # connect to the server on local computer
    s.connect((ip_addr, port))
    # receive data from the server
    msg = s.recv(2048).decode()
    print(msg)
    # close the connection
    s.close()


def main():
    get_host_info()
    connect_to_server("www.google.com", 80)
    connect_to_server_v2("djxmmx.net", 17)
    connect_to_server_v2("ntp-b.nist.gov", 13)


if __name__ == "__main__":
    main()
