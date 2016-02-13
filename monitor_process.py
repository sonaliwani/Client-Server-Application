#!/usr/bin/env python
"""
Monitor Process
"""

import socket
import time
import re
import sys

port = 50000
size = 1024

'''
Function        : command_help
Input           : None
Definition      : List of commands supported
'''
def command_help():
        print ('monitor <hostname>      : To connect to Monitor')
        print ('get                     : To get the current simulator value')
        print ('set <value>             : To set the current simulator value')
        print ('stop                    : To stop the simulator running')
        print ('continue                : To continue the simualtor running')
        print ('quit                    : To quit from Monitor')

'''
Function        : is_valid_hostname
Input           : hostname
Definition      : Verifies if hostname provided by user is valid
'''
def is_valid_hostname(hostname):
        if len(hostname) > 255:
                return False
        if hostname[-1] == ".":
                hostname = hostname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

print (' This is the Monitor Process ')
command_help()
connected = False

while True:
        print ('Please Enter Command to be executed')
        line = input()
        if not line:
                continue
        args = line.split()
        if args[0] == 'get':
                if len(args) > 1:
                        print ('Get command cannot have more arguments')
                        command_help()
                        continue
        elif args[0] == 'set':
                if len(args) != 2:
                        print ('set command not used properly')
                        command_help()
                        continue
                try:
                        val = int(args[1])
                except ValueError:
                        print("Please pass an integer")
                        continue
        elif args[0]  == 'stop':
                if len(args) > 1:
                        print ('stop command not used properly')
                         command_help()
                         continue
        elif args[0] == 'continue':
                if len(args) > 1:
                        print ('continue command not used properly')
                        command_help()
                        continue
        elif args[0] == 'quit':
                if len(args) > 1:
                        print ('continue command not used properly')
                        command_help()
                        continue
                break
        elif args[0] == 'monitor':
                print ('In monitor ....')
                if connected:
                        print (' Already connected to a Server, you cannot connect to 2 servers at a time')
                        continue
                if len(args) != 2:
                        print ('monitor command not used properly')
                        command_help()
                        continue
                hostname = args[1]
                if is_valid_hostname(hostname):
                        host = hostname
                        try:
                                #Connect to the required Host using Socket
                                #SOCK_STREAM we want a TCP Socket
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.connect((host,port))
                                connected = True
                        except socket.error:
                                if s:
                                        s.close()
                                        print ("Could not open socket: ")
                                        sys.exit(1)
                else:
                        print ('Invalid hostname')

        else:
                print ('Unknown command, command not supported')
                command_help()
                continue
        if connected :
                s.send(line.encode('ascii'))
                resp = s.recv(size)
                data = resp.decode('ascii')
                print ('Received:', data)
        else :
                print ('Not connected to any Server please connect before running any other command')
s.close()




