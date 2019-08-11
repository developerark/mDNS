class IServer:
    def onJoin():
        '''
        When server receives a join broadcast from a peer
        '''
        raise NotImplementedError("Subclass needs to implement onJoin()")

    def onLeave():
        '''
        When server receives a leave broadcast from a peer
        '''
        raise NotImplementedError("Subclass needs to implement onLeave()")
