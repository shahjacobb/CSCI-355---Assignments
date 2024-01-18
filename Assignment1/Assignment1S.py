"""
Queens College
Internet and Web Technology (CSCI 355)
Winter 2024
Assignment1S - Socket Programming, Server Side
Shah Bhuiyan
"""
import socket
# [6] Write a program, Assignment2Server.py. https://www.geeksforgeeks.org/socket-programming-python/
def run_server(port):
    # create a socket object
    s = socket.socket()
    print("Socket successfully created")

    # Next, bind to the port, but no IP so we can listen to requests from anywhere
    s.bind(('', port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until we interrupt it or an error occurs
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)

        # send a thank you message to the client.
        c.send('Thank you for connecting'.encode())

        # Close the connection with the client
        c.close()
        break


def main():
    run_server(80)

if __name__ == "__main__":
    main()


#  1 2 3 4 5 6 7 8 9 10 11 mid = 6, target = 8
#   6 7 8 9 10 11 low = 6, mid = 9,
#