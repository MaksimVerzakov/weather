from twilix.stanzas import Presence
from twilix.base import WrongElement, EmptyStanza

from weather import UnknownCityException
from weather import GoogleException


class MyPresence(Presence):
    
    def probeHandler(self):
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result, 'available')
        deff.addErrback(self.error)
        return EmptyStanza()
       
    def subscribeHandler(self):        
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.received_condition)
        deff.addErrback(self.error)
        return EmptyStanza()
    
    def received_condition(self, condition):
        print 'received'
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
        reply3 = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_='subscribe',                          
                        )
        self.host.dispatcher.send((reply1, reply2, reply3))
    
    def subscribedHandler(self):
        self.host.addSubscr(self.from_, self.to)
        return EmptyStanza()

    def availableHandler(self):
        self.host.addOnlinesubscr(self.from_, self.to)
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result, 'available')
        deff.addErrback(self.error)
        return EmptyStanza()
        
    def unavailableHandler(self):
        self.host.rmOnlinesubscr(self.from_, self.to)
        return EmptyStanza()
            
    def unsubscribeHandler(self):
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_='unsubscribed',                          
                        )
        self.host.rmSubscr(self.from_, self.to)
        return EmptyStanza()
    
    def result(self, respond, type):
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_=type,
                          status = respond,
                        )
        self.host.dispatcher.send(reply)
    
    def error(self, err):
        fail = err.trap(UnknownCityException, GoogleException)
        if fail == UnknownCityException:
            reply = Presence(
                             to=self.from_,
                             from_=self.to,
                             type_='unsubscribed',                          
                            )
            self.host.dispatcher.send(reply)
        if fail == GoogleException:
            reply = Presence(
                             to=self.from_,
                             from_=self.to,
                             type_='error',                          
                            )
            self.host.dispatcher.send(reply)
