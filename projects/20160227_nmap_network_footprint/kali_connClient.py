#!/usr/bin/env python3
#
# Authenticate a list of emails on a server
# Usage Scenarios:
#   [0]: kali_connClient.py
#   [1]: kali_connClient.py <listemails.txt>
#
#   Author: Devin Trejo
#   20160227

import socket, sys


def main(argv):
    # Client machine
    #
    clientIP = "10.10.10.102"

    # Check whether to run as example or to open from file
    #
    if len(argv) ==  1:
        listEmails = ["test@localhost", "admin@localhost", \
                "root@localhost", "htpp@locahost", "ftp@locahost",
                "nfs@localhost", "mysql@localhost", ]
    else:
        listEmails = []
        with open(argv[1]) as f:
            for line in f:
                listEmails.append(line)

    validEmails = tryListEmail(clientIP, listEmails)

    print("Valid emails are: \n" + str(validEmails))
    return

def tryListEmail(clientIP, listEmails):
    BUFFER_SIZE = 1024
    clientPORT = 25

    # Create a list to store valid IPs
    #
    validEmails = []

    # Loop for all emails in our list
    #
    for userEmail in listEmails:
        # Connect to server
        #
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((clientIP, clientPORT))
        except Exception:
            print("Connection Error")
            s.close()
            return -1

        # Recieve Greeting
        #
        data = s.recv(BUFFER_SIZE)
        print("S: " + bytes.decode(data, 'UTF-8').rstrip('\r\n'))

        # Send EHLO MSG
        #
        msgCmd = "EHLO mail.localdomain\n"
        #msgCmd = "helo hi\n"
        print("C: " + msgCmd.rstrip('\r\n'))
        s.send(bytes(msgCmd, 'UTF-8'))

        # Wait for EHLO Response
        #
        data = s.recv(BUFFER_SIZE)
        print("S: " + bytes.decode(data, 'UTF-8').rstrip('\r\n'))

        # Send MSG from
        #
        msgCmd = ("mail from: <root@localhost>\n")
        s.send(bytes(msgCmd, 'UTF-8'))
        print("C: " + msgCmd.rstrip('\r\n'))

        # Wait for MSG from reponse
        #
        data = s.recv(BUFFER_SIZE)
        print("S: " + bytes.decode(data, 'UTF-8').rstrip('\r\n'))

        # Send Recpt
        msgCmd = ("rcpt to: <" + userEmail + ">\n")
        s.send(bytes(msgCmd, 'UTF-8'))
        print("C: " + msgCmd.rstrip('\r\n'))

        # Wait for Server Reponse
        #
        data = s.recv(BUFFER_SIZE)
        data = bytes.decode(data, 'UTF-8').rstrip('\r\n')
        print("S: " + data)

        # Check if message contains success
        #
        if 'Ok' in data:
            validEmails.append(userEmail)
        # Close connection
        #
        msgCmd = "quit\n"
        s.send(bytes(msgCmd, 'UTF-8'))
        print("C: " + msgCmd.rstrip('\r\n'))
        data = s.recv(BUFFER_SIZE)
        print("S: " + bytes.decode(data, 'UTF-8'))
        s.close()
    return validEmails