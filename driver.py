from sender import transmit_message
from receiver import listenForData
from convertUtility import bytesToMessage, messageToBytes
import threading

def listen(port):
    listenForData(port)

def broadcast(message, username, ports):
    transmit_message(messageToBytes("[" + username + "]: " + message), ports)

def receiveAllPorts():
    p1 = threading.Thread(target=listen, args=(1,))
    p2 = threading.Thread(target=listen, args=(2,))
    p3 = threading.Thread(target=listen, args=(3,))
    p4 = threading.Thread(target=listen, args=(4,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()


def broadcastAllPorts(message, username):
    b1 = threading.Thread(target=broadcast, args=(message, username, [1,2,3,4]))
    
    b1.start()
    b1.join()
