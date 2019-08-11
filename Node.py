from IServer import IServer
from IPeer import IPeer

class Node(IServer, IPeer):
    def __init__(self, name, port=8080):
        '''
        Creates a P2P Node

        Args:
            name (str): The human readable name of the Node
            port (int): The port on which the server of a P2P Node runs on
        '''
        self.__name = name
        self.__port = port

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

if __name__ == "__main__":
    node = Node("Aswin's iPhone")
