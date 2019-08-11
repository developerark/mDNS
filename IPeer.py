class IPeer:
    def join():
        '''
            When peer joins the network
        '''
        raise NotImplementedError("Subclass needs to implement join()")

    def leave():
        '''
            When peer leaves the network
        '''
        raise NotImplementedError("Subclass needs to implement leave()")
