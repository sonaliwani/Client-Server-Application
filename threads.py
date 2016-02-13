#!/usr/bin/python
'''
Python Module   : threads
Purpose         : Defined Classes to manage threads for Server and Simulator
'''
import threading
import time
from random import randint
count = 0
'''
Class           : myThread
Parent Class for setting up the threadID and name
'''
class myThread (threading.Thread):
        def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                pass

'''
Class           : serverThread
This class handles the logic for Server Thread
'''

class serverThread(myThread):
        def __init__(self, threadID, name, conn, stop_event):
                myThread.__init__(self, threadID, name)
                self.conn = conn
                self.stop_event = stop_event
        def run(self):
                print ("Starting " + self.name)
                serve_client(self.conn, self.stop_event)
                print ("Exiting ..........." + self.name)

'''
Class           : simulatorThread
Inherited from  : myThread
This class handles the logic for Simulator Thread
'''
class simulatorThread(myThread):
        def __init__(self, threadID, name, stop_event, kill_event):
                myThread.__init__(self, threadID, name)
                self.stop_event = stop_event
                self.kill_event = kill_event
 def run(self):
                print ("Starting " + self.name)
                simulator_thread(self.stop_event, self.kill_event)
                print ("Exiting " + self.name)

'''
Function                : simulator_thread
Input              : stop_event, kill_event
Definition        : Simulator code which increments "count" and sleeps for random time between 1 and 5
                  It is also listening on events stop_event and kill_event
                  On receiving kill_event, the thread stops and exists
                  On receiving stop_event, the thread is blocked
'''
def simulator_thread(stop_event, kill_event):
        global count
        while True:
                stop_event.wait()
                count = count + 1
                time.sleep(randint(1,5))
                print (count)
                if kill_event.isSet():
                        break
'''
Function                : serve_client
Input              : conn
Definition        : Is the thread responsible for listening to the Monitor Process
'''
def serve_client(conn, stop_event):
        
        '''
        stop_event = threading.Event()
        kill_event = threading.Event()
        '''
        global count
        #count = 0
        '''
        thread2 = simulatorThread(99, "simulator-thread", stop_event, kill_event)
        thread2.start()
        stop_event.set()
        '''
        #infinite loop so that function do not terminate and thread do not end.
        while True:
                #Receiving from client
                resp = conn.recv(1024)
 if not resp:
                        break
                data = resp.decode('ascii')
                print ('Server side : Received message ', data)
                args = data.split()
                if args[0] == 'get':
                        reply = 'Current Simulator value is :' + str(count)
                elif args[0] == 'stop':
                        # Send a clear event, so Simulator will be blocked and will stop doing
                        # its task
                        stop_event.clear()
                        reply = 'Stop received ...'
                elif args[0] == 'continue':
                        stop_event.set()
                        reply = 'Continue received ...'
                elif args[0] == 'set':
                        stop_event.clear()
                        count = int(args[1])
                        stop_event.set()
                        reply = 'Set simulator value at :' +  str(count)
                else:
                        reply = 'Receive Connection'
 conn.send(reply.encode('ascii'))

        #came out of loop
        print ('Connection closed by client')
        #Make sure anyone listening to these events in unblocked.
        #kill_event.set()
        stop_event.set()
        conn.close()
