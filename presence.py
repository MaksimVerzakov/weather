from twilix.stanzas import Presence
from twilix.base import WrongElement, EmptyStanza


class MyPresence(Presence):
    
    def probeHandler(self):
        print 'probe'
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result, 'available')
        deff.addErrback(self.err)
        return EmptyStanza()
       
    def subscribeHandler(self):
        reply1 = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_='subscribed',                          
                        )
        reply2 = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_='subscribe',                          
                        )
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result, 'available')
        return (reply1, reply2)
    
    def subscribedHandler(self):
        self.host.addSubscr(self.from_, self.to)
        return EmptyStanza()

    def availableHandler(self):
        print 'avail'
        self.host.addOnlinesubscr(self.from_, self.to)
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result, 'available')
        return EmptyStanza()
        
    def unavailableHandler(self):
        print 'unavail'
        self.host.rmOnlinesubscr(self.from_, self.to)
        return EmptyStanza()
            
    def unsubscribeHandler(self):
        print 'unsubscr'
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_='unsubscribed',                          
                        )
        self.host.rmSubscr(self.from_, self.to)
        return EmptyStanza()
    
    def result(self, respond, type):
        print respond
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_=type,
                          status = respond,
                        )
        self.host.xmlstream.send(reply)
    
    def err(self, error):
        print 'error %s' % error

