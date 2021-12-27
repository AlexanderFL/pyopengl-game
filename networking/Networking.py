from json.decoder import JSONDecodeError
import socket
import json
from objects.Player import Player
from objects.Bullet import Bullet
from time import time

class Networking:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connected = False
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.timer = time()
        self.server_rate = 240
        self.server_counter = 0

        self.buffer = []

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            self.socket.setblocking(0)
        except TimeoutError as timeout:
            print(timeout.strerror)
            return -1
        except InterruptedError as interrupt:
            print(interrupt.strerror)
            return -1
        except ConnectionRefusedError as refused:
            print("Couldn't connect to %s:%s... server might be offline, try again later" % (self.ip, str(self.port)))
            print("Exception info: %s" % (refused.strerror))
            return -1
        
        self.connected = True
        return 1
    
    def send_on_next_update(self, object):
        if object not in self.buffer:
            self.buffer.append(object)
    
    async def update(self):
        # Update the server 240 times per second
        current_time = time()
        data = None
        if current_time > self.timer + self.server_counter / float(self.server_rate):
            for object in self.buffer:
                if type(object) == Player:
                    object_ser = self.serialize_player_data(object)
                    self.send(object_ser)
                elif type(object) == Bullet:
                    object_ser = self.serialize_bullet_data(object)
                    self.send(object_ser)
            self.buffer.clear()

            data = self.recv()
            self.server_counter += 1
        if self.server_counter > self.server_rate - 1:
            self.timer = time()
            self.server_counter = 0
        
        return data

    def serialize_player_data(self, player_data : Player):
        if type(player_data) == Player:
            new_dict = { 
                "player": player_data.get_dict()
            }
            return json.dumps(new_dict)
    
    def serialize_bullet_data(self, bullet_data : Bullet):
        new_dict = {
            "bullet": bullet_data.get_dict()
        }
        return json.dumps(new_dict)
        
    
    def recv(self):
        data = None
        try:
            data = self.socket.recv(1024)
        except BlockingIOError as ioblock:
            return None

        if not data:
            return None
        data = data.decode('utf-8')

        try:
            data = json.loads(data)
            print(data)
        except JSONDecodeError as error:
            print("Recv() error -> %s, data recieved: %s" % (error.msg, data))
            return None
        
        return data
    
    def send(self, data:str):
        try:
            self.socket.sendall(bytes(str(data), encoding="utf-8"))
            return 1
        except Exception as e:
            print(e.with_traceback)
            return -1