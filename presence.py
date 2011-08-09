from twilix.stanzas import Presence
from twilix.base import WrongElement, EmptyStanza


class MyPresence(Presence):
    
    def probeHandler(self):
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result, 'subscribed')
        return EmptyStanza()
       
    def subscribeHandler(self):
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_='subscribed',                          
                        )
        self.host.addSubscr(self.from_, self.to)
        deff = self.host.wbase.get_condition(self.to.user)
        deff.addCallback(self.result,'available')
        return reply
    
    def unsubscribeHandler(self):
        self.host.rmSubscr(self.from_, self.to)
    
    def result(self, respond, type):
        print respond
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_=type,
                          status = str(respond),
                        )
        self.host.xmlstream.send(reply)

