#!/usr/bin/python

import threading
import time
import socket
import sys
from threads import *
from threads import myThread
from threads import simulatorThread
from threads import serverThread

'''
Main Simulator Process
'''


HOST = ''
PORT = 50000

stop_event = threading.Event()
kill_event = threading.Event()

thread2 = simulatorThread(99, "simulator-thread", stop_event, kill_event)
thread2.start()
stop_event.set()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit(1)

print ('Socket bind complete')

#Start listening on socket
s.listen(10)
print ('Socket now listening')
thread_count = 0
while 1:

 #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    # Create new threads
    server_thread = serverThread(thread_count + 1, "Thread"+str(thread_count), conn, stop_event)
    thread_count = thread_count + 1

# Start new Threads
    server_thread.start()
kill_event.set()
s.close()

