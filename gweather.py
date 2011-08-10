import time
import os

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.words.xish import domish,xpath
from twisted.words.xish.domish import Element
from twisted.words.protocols.jabber import xmlstream, client, jid, component

from twilix.stanzas import Message, Iq, Presence
from twilix.base import WrongElement
from twilix.jid import internJID
from twilix.version import ClientVersion

from twilix.roster import Roster
from twilix.dispatcher import Dispatcher
from twilix.vcard import VCard, VCardQuery

from presence import MyPresence
from subscribed import SubscribedList
from weatherbase import WeatherBase

class WeatherComponent(component.Service):
    def __init__(self, reactor, version, config, cJid):
        self.config = config
        self.reactor = reactor
        self.VERSION = version
        self.cJid = internJID(cJid)
        self.startTime = None
        self.xmlstream = None
        self.subscribed = SubscribedList(config)
        self.wbase = WeatherBase()
        self.online = []   
        
    def componentConnected(self, xs):
        self.startTime = time.time()
        self.xmlstream = xs
        self.dispatcher = Dispatcher(xs, self.cJid)
        self.dispatcher.registerHandler((MyPresence, self))
        self.dispatcher.registerHandler((Message, self))
        self.getOnline()
        self.lc = task.LoopingCall(self.updateStatus)
        self.lc.start(900)
        print 'Connected'

    def addSubscr(self, from_, to):
        self.subscribed.add_subscr(from_, to)
    
    def rmSubscr(self, from_, to):
        self.subscribed.rm_subscr(from_, to)
    
    def addOnlinesubscr(self, from_, to):
        self.online.append((from_, to))
            
    def rmOnlinesubscr(self, from_, to):
        self.online.remove((from_, to))
    
    def getOnline(self):
        for from_, to in self.subscribed.subscr_list:
            reply = Presence(
                          to=from_,
                          from_=to,
                          type_='probe',                          
                        )
            self.xmlstream.send(reply)
    
    def updateStatus(self):
        for from_, to in self.online:
            deff = self.wbase.get_condition(to.user)
            deff.addCallback(self._result, from_, to)
    
    def _result(self, respond, from_, to):
        reply = Presence(
                          to=from_,
                          from_=to,
                          status=respond,                          
                        )
