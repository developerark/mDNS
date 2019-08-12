from IServer import IServer
from IClient import IClient
import socket
from threading import Thread, Lock
import json
import argparse
import time

BUFFERSIZE = 65535

class Peer(IServer, IClient):
    def __init__(self, name, port=8080):
        '''
        Creates a P2P Node

        Args:
            name (str): The human readable name of the Node
            port (int): The port on which the server of a P2P Node runs on
        '''
        self.__name = name
        self.__port = port
        # name -> IP on the network
        self.__MDNSCache = {}

    def __iter__(self):
        yield "name", self.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    # Server methods
    def __startListening(self):
        # Setup socket and bind
        self.__listenerUDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__listenerUDPSocket.bind(('0.0.0.0', self.port))
        print('Listening for messages at {}'.format(self.__listenerUDPSocket.getsockname()))

        # Start receiving messages
        while True:
            data, address = self.__listenerUDPSocket.recvfrom(BUFFERSIZE)
            if address == None:
                return

            text = data.decode('ascii')
            print('The client at {} says: {}'.format(address, text))
            try:
                message = json.loads(text)

                action = message["action"]
                fromPeer = message["fromPeer"]
                fromPeer.update({"address": address[0]})
                if action == "join":
                    self.onJoin(fromPeer)
                elif action == "leave":
                    self.onLeave(fromPeer)
                elif action == "ping":
                    self.onPing(fromPeer)
            except Exception as error:
                print(str(error))


    def onJoin(self, peer):
        self.__MDNSCache.update({peer["name"]: peer["address"]})
        self.ping(peer)
        print(self.__MDNSCache)

    def onLeave(self, peer):
        try:
            self.__MDNSCache.pop(peer["name"])
        except KeyError as exception:
            # Keyerror when not found. Does not matter
            pass
        print(self.__MDNSCache)

    def onPing(self, peer):
        self.__MDNSCache.update({peer["name"]: peer["address"]})
        print(self.__MDNSCache)

    # Client methods
    def join(self):
        '''
        Once instanciated, this method is called which will broadcast to the
        network that it has joined the network
        '''
        # Start the listener thread before broadcast
        self.__listenerThread = Thread(target=self.__startListening, daemon=True)
        self.__listenerThread.start()

        # Give the listener some time to load
        time.sleep(3)

        # Broadcast that you are joining the network
        UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        text = json.dumps({
            "action": "join",
            "fromPeer": {
                "name": self.name,
            }
        })
        UDPSocket.sendto(text.encode('ascii'), ('<broadcast>', self.__port))

    def leave(self):
        UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        text = json.dumps({
            "action": "leave",
            "fromPeer": {
                "name": self.name,
                }
        })
        UDPSocket.sendto(text.encode('ascii'), ('<broadcast>', self.__port))

        # Give the listeners some time to remove yourself
        time.sleep(3)

        try:
            self.__listenerUDPSocket.shutdown(socket.SHUT_RDWR)
            self.__listenerUDPSocket.close()
        except Exception as exception:
            pass

    def ping(self, peer):
        UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        text = json.dumps({
            "action": "ping",
            "fromPeer": {
                "name": self.name
            }
        })
        UDPSocket.sendto(text.encode('ascii'), (peer["address"], self.port))

if __name__ == "__main__":
    # Argument Parser setup
    parser = argparse.ArgumentParser()
    parser.add_argument("deviceName", type=str, help="A unique name for the device")
    args = parser.parse_args()

    peer = Peer(args.deviceName)
    peer.join()

    input("")

    peer.leave()
