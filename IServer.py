import abc

class IServer(abc.ABC):

    @abc.abstractmethod
    def onJoin(self, peer):
        '''
        When server receives a join broadcast from a peer
        '''
        pass

    @abc.abstractmethod
    def onLeave(self, peer):
        '''
        When server receives a leave broadcast from a peer
        '''
        pass

    @abc.abstractmethod
    def onPing(self, peer):
        '''
        When peer pings saying they are alive
        '''
