__author__ = "Ayush Agrawal, Andrew Bryan, Justin Carter, Christopher DeLaGarza, Deep Desai, Zachray Gray, Joshua Harlan, Ryan Jacobs, 
Ryan King, Iori Koh, Sarath Muddana, Ryan Noeske, Brett Phillips, Devin Popock, Alyssa Rios, Ammar Sheikh, Cosme Tejeda, Ryan Vanek"
__past_authors_2017__ = "Kyle Coffey, Zitao Fang, Chris Jung, Taaha Kamal, Maximilian Patrick, Weston Reed, Tanvir Towhid, Vance Vaughn, 
Abhi Velaga, Jacob Waller, Colin Zhong"
_teacher_ = "Taylor Hudson"
__credits__ = ["Ayush Agrawal", "Andrew Bryan", "Justin Carter", "Christopher DeLaGarza", "Deep Desai", "Zachray Gray", 
"Joshua Harlan", "Ryan Jacobs", "Ryan King", "Iori Koh", "Sarath Muddana", "Ryan Noeske", "Brett Phillips", "Devin Popock", 
"Alyssa Rios", "Ammar Sheikh", "Cosme Tejeda", "Ryan Vanek", "Kyle Coffey", "Zitao Fang", "Chris Jung", "Taaha Kamal", 
"Maximilian Patrick", "Weston Reed", "Tanvir Towhid", "Vance Vaughn", "Abhi Velaga", "Jacob Waller", "Colin Zhong", "Taylor Hudson"]
__copyright__ = "Copyright 2017, Allen High School Co-cirruclar Project"
__license__ = "GPL"
__version__ = "2.0.5"
__maintainer__ = "Christopher DeLaGarza, Deep Desai, Taylor Hudson"
__email__ = "Taylor.Hudson@allenisd.org"
__status__ = "Project Used"

##Sense Hat code by Computer Science 3 Class of 2017
##Special Appearance by Tanvir Towhid
##Special Thanks to Mr. Hudson
import socket
import threading
import sys
from sense_hat import SenseHat
import queue
import time

sense = SenseHat()
clientAmmount = 2
for i in range(1, clientAmmount + 1):
    print(i)

queues = []

for i in range(1, clientAmmount + 1):
    queues.append(queue.Queue(maxsize = 10))

addresses = []
for i in range(clientAmmount):
    if i != 4:
        addresses.append('192.168.1.' + str(i + 2))
        print(addresses[i])

queueHandshake = queue.Queue(maxsize = clientAmmount) #change maxsize according to the number of pi's on network 

def FullScreen(R,G,B): #This means red, green, and blue
    Color = [R, G, B]
    screen = [
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
    ]
    sense.clear()
    sense.set_pixels(screen)
    time.sleep(1)
    sense.load_image('Tanvir.png')
    return

class ThreadedServer(object):
    def __init__(self, host, port): #Initialize all variables in ThreadedServer
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.size = 1024

    def listen(self): #listens for clients
        self.sock.listen(5)
        check = True

        q = []
        clients = []
        for i in range(1, clientAmmount + 1):
            q.append(True)
            
        whileFinish = False
        while not whileFinish: #while loop only runs if all clients are not accepted
            client, address = self.sock.accept()
            addresshost, addressport = address
            print(addresshost)
            
            #identifying and saving different clients
            #to send go message
            for i in range(clientAmmount):
                if addresshost == addresses[i]:
                    clients.append(client)
                    FullScreen(0, 255, 0)
                    print(addresshost, ':' + str(i))
            
                
            client.settimeout(60)
            
            #check for handshake
            #when server recieves client communication it will hold the server
            #once all clients are signed in this if-statement sends a go message
            #to clients that will trigger the clients to send data.
            #The server the client handshake in this way.
            if not queueHandshake.full():
                for i in range(clientAmmount):
                    if addresshost == addresses[1] and q[i]:
                        queueHandshake.put(True)
                
##                if queue3.qsize() != 0 and q3 :
##                    queueHandshake.put(True)
##                    q3 = False
##                if queue4.qsize() != 0 and q4 :
##                    queueHandshake.put(True)
##                    q4 = False
##                if queue5.qsize() != 0 and q5 :
##                    queueHandshake.put(True)
##                    q5 = False


                if queueHandshake.full():
                    print('handshake acheived')
                    for i in range(clientAmmount):
                        clients[i].sendall(bytes('in', 'utf-8'))
                        time.sleep(2.0)
##                    time.sleep(2.0)
##                    client3.sendall(bytes('in', 'utf-8'))
##                    time.sleep(2.0)
##                    client4.sendall(bytes('in', 'utf-8'))
##                    time.sleep(2.0)
##                    client5.sendall(bytes('in', 'utf-8'))

            #The server starts a thread for each client.      
            if queueHandshake.full(): #Starts recieving information after all pis are connected
                print('Thread Start')
                for i in range(clientAmmount):
                    threading.Thread(target = handler, args = (clients[i], i)).start()
                threading.Thread(target = queues, args = ()).start()
##                threading.Thread(target = handler, args = (client3, 3))
##                threading.Thread(target = handler, args = (client4, 4))
##                threading.Thread(target = handler, args = (client5, 5))
                whileFinish = True
            

#This function runs in a separate thread and reads data from the queues.
def queues(): #This is a queue. We use it to queue things.
    b = 0;
    while True: 
        if queueHandshake.full():
            sense.show_message('go', scroll_speed = .01, text_colour = [255, 180, 50])
            for i in range(clientAmmount):
                if not queues[i].empty():
                    displayStr = str(queues[i].get(block = True, timeout = None))
                    displayStr = displayStr[2:len(displayStr)-1]
                    print('Received from ', addresses[i], ' : ', displayStr)
            
                #sense.show_message(displayStr, scroll_speed = .1, text_colour = [255, 180, 50],)

##            if not queue3.empty():
##                displayStr = str(queue3.get(block = True, timeout = None))
##                displayStr = displayStr[2:len(displayStr)-1]
##                print(sys.stderr, 'received from 192.168.1.5 : ', displayStr)
##                sense.show_message(displayStr, scroll_speed = .1, text_colour = [255, 180, 50],)
##            if not queue4.empty():
##                displayStr = str(queue4.get(block = True, timeout = None))
##                displayStr = displayStr[2:len(displayStr)-1]
##                print(sys.stderr, 'received from 192.168.1.6 : ', displayStr)
##                sense.show_message(displayStr, scroll_speed = .1, text_colour = [255, 180, 50],)
##
##            if not queue5.empty():
##                displayStr = str(queue5.get(block = True, timeout = None))
##                displayStr = displayStr[2:len(displayStr)-1]
##                print(sys.stderr, 'received from 192.168.1.7 : ', displayStr)
##                sense.show_message(displayStr, scroll_speed = .1, text_colour = [255, 180, 50],)


#Each client will put their data in the queue that is reserved for them
def handler (client, clientNum):
    while True:
        data = client.recv(1024)
        queues[clientNum - 1].put(data)
       

print(sys.stderr, 'Server Starting')
sense.load_image('Tanvir.png')
server1 = ThreadedServer(host = '192.168.1.4', port = 10000)
server1.listen()
sense.clear()
