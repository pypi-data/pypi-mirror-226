import socket
import time

from cc.serializer import SocketSerializer

class SocketConnection:
    def __init__(self, ip_address):
        self.s = None
        self.ip_address = ip_address
        self.port = 5025
    
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        addr = (self.ip_address, self.port)
        try:
            self.s.connect(addr)
        except socket.error as e:
            print("failed to connect: ", addr)
            print(e)
        
        return self.s

    def close(self):
        self.s.close()
    
    def getIDN(self):
        self.s.sendall(b"*IDN?\n")
        data = self.s.recv(1024)
        return data.decode()

    def getInstrumentIdentification(self):
        return self.getIDN()
    
