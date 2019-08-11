import abc

class IServer(abc.ABC):

    @abc.abstractmethod
    def onJoin(self):
        '''
        When server receives a join broadcast from a peer
        '''
        pass

    @abc.abstractmethod
    def onLeave(self):
        '''
        When server receives a leave broadcast from a peer
        '''
        pass
