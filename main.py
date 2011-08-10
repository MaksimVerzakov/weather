#!/usr/bin/python
# Google Weather Jabber-service
#
# copyright 2011 Verzakov Maxim aka xam_vz 
#
# License: GPL-v3
#
import getopt
import os
import sys
import ConfigParser

from twisted.words.protocols.jabber import component
from twisted.internet import reactor
from twisted.scripts import _twistd_unix as twistd

import gweather

def main():
    config = ConfigParser.ConfigParser()
    config.read('weather.conf')
    jid = config.get('component', 'jid')
    password = config.get('component', 'password')
    host = config.get('component', 'host')
    port = config.get('component', 'port')
    path = config.get('component', 'basepath')
    c = gweather.WeatherComponent(reactor, version, config, jid)
    f = component.componentFactory(jid, password)
    connector = component.buildServiceManager(jid, password,
                                     "tcp:%s:%s" % (host, port))
    c.setServiceParent(connector)
    connector.startService()
    reactor.run() 

if __name__ == "__main__":
    main()
