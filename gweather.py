import time
import os

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
        self.suscribed = SubscribedList(os.path.dirname(__file__) + '/subscribed.txt')
        self.wbase = WeatherBase()        
        
    def componentConnected(self, xs):
        self.startTime = time.time()
        self.xmlstream = xs
        self.dispatcher = Dispatcher(xs, self.cJid)
        self.dispatcher.registerHandler((MyPresence, self))
        self.dispatcher.registerHandler((Message, self))
        print 'Connected'

    def addSubscr(self, from_, to):
        self.suscribed.add_subscr(from_, to)
    
    def rmSubscr(self, from_, to):
        self.suscribed.rm_subscr(from_, to)
    
    def updateStatus(self):
        els = []
        for from_, to in self.subscribed.subscr_list:
            els.append(Presence(to=self.from_,
                                from_=self.to,
                                type_='available',
                                status='')
                      )
        

if __name__ == '__main__':
    print "start main.py"
    sys.exit(0)
