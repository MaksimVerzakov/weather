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

#from ossignal import install_shutdown_handlers
import gweather

def main():
    version = "0.1"

    from optparse import OptionParser
    parser = OptionParser(version=
                          "Habahaba-ng component version:" + version)
    parser.add_option('-c', '--config', metavar='FILE', dest='configFile',
                      help="Read config from custom file")
    parser.add_option('-b', '--background', dest='configBackground',
                      help="Daemonize/background transport",
                      action="store_true")
    (options,args) = parser.parse_args()
    configFile = options.configFile
    configBackground = options.configBackground

    config = ConfigParser.ConfigParser()
    if configFile:
        config.read(configFile)
    else:
        config.read('weather.conf')
    if configBackground and os.name == "posix": # daemons supported?
        twistd.daemonize() # send to background
    try:
        pid_file = config.get('process', 'pid', None)
    except:
        pid_file = None
    if pid_file:
        pid = str(os.getpid())
        pidfile = open(pid_file, "w")
        pidfile.write("%s\n" % pid)
        pidfile.close()

    jid = config.get('component', 'jid')
    password = config.get('component', 'password')
    host = config.get('component', 'host')
    port = config.get('component', 'port')
    c = gweather.WeatherComponent(reactor, version, config, jid)
    f = component.componentFactory(jid, password)
    connector = component.buildServiceManager(jid, password,
                                     "tcp:%s:%s" % (host, port))
    c.setServiceParent(connector)
    connector.startService()
    #install_shutdown_handlers(c.shuttingDown)
    reactor.run() #installSignalHandlers=False)

if __name__ == "__main__":
    main()
