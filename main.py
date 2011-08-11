#!/usr/bin/python
# Google Weather Jabber-service
#
# copyright 2011 Verzakov Maxim aka xam_vz 
#
# License: GPL-v3kiev
#
import ConfigParser

from twisted.words.protocols.jabber import component
from twisted.internet import reactor

import gweather

def main():
    version = '0.3'
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
