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
        deff.addErrback(self.error)
        return (reply1, reply2)
    
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
        self.host.xmlstream.send(reply)
    
    def error(self, err):
        self.result(err.getErrorMessage(), 'unavailable')
