import abc

class IClient(abc.ABC):

    @abc.abstractmethod
    def join(self):
        '''
        When peer joins the network
        '''
        pass

    @abc.abstractmethod
    def leave(self):
        '''
        When peer leaves the network
        '''
        pass

    @abc.abstractmethod
    def ping(self, peer):
        '''
        Ping the peers listener back saying you are alive
        '''
