from twisted.internet.defer import inlineCallbacks, returnValue

from twilix.stanzas import Presence
from twilix.base import WrongElement, EmptyStanza

from weather import UnknownCityException
from weather import GoogleException


class MyPresence(Presence):
    
    @inlineCallbacks
    def probeHandler(self):
        try:
            condition = yield self.host.wbase.get_condition(self.to.user)
            type = 'available'
        except (UnknownCityException, GoogleException) as err:
            condition, type = self._error(err)           
               
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_=type,
                          status = condition,
                        )
        returnValue(reply)
    
    @inlineCallbacks   
    def subscribeHandler(self):
        try:
            condition = yield self.host.wbase.get_condition(self.to.user)
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
                          type_='available',
                          status = condition
                        )
            reply = (reply1, reply2, reply3)
        except (UnknownCityException, GoogleException) as err:
            condition, type = self._error(err)
            reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_=type,                          
                        )
        returnValue(reply)
    
    def subscribedHandler(self):
        self.host.addSubscr(self.from_, self.to)
        return EmptyStanza()

    @inlineCallbacks
    def availableHandler(self):
        self.host.addOnlinesubscr(self.from_, self.to)
        try:
            condition = yield self.host.wbase.get_condition(self.to.user)
            type = 'available'
        except (UnknownCityException, GoogleException) as err:
            condition, type = self._error(err)
        reply = Presence(
                          to=self.from_,
                          from_=self.to,
                          type_=type,
                          status = condition,
                        )
        returnValue(reply)
        
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
    
    def _error(self, err):
        condition = ''
        if isinstance(err, UnknownCityException):
            type='unsubscribed'
        if isinstance(err, GoogleException):
            type='error'
        return (condition, type)
