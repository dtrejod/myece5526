#!/usr/bin/env python3
import socket, sys, os


def main():
    # Client machine IPv4 address
    #
    clientIP = 10.10.10.102
    clinetPORT = 25

    # Declare a acceptable buffer size that fits into TCP Packet
    #
    BUFFER_SIZE = 1024

    # Create a new socket to the server
    #
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect to passed IP
    #
    try:
        s.connect((clientIP, clinetPORT))
    except Exception:
        s.close()
        return -1

    # Check to see if the a name exists on the remote machine
    #
    for userEmail in listEmails:
        msgCmd = "220 " + username + " ESMTP"

        s.send(bytes(msgCmd, 'UTF-8'))

        # Wait to receive a message
        data = s.recv(BUFFER_SIZE)
        data =  bytes.decode(data, 'UTF-8')
        print("Received data: \n" + data)

