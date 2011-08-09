# -*- coding: utf8 -*-
import os

import twisted.web.client
from twisted.internet import reactor, task
from twisted.internet import defer
from xml.dom.minidom import parseString

class UnknownCityException(BaseException):
    pass

class GoogleException(BaseException):
    pass

class Weather(object):
    """Class weather gets current weather condition data from
    Google Weather API.    
    """
    def __init__(self, city):
        self.city = city             

    def get_weather(self):
        """Send GET request to Google Weather API.         
        """
        self.result = defer.Deferred()
        deff = twisted.web.client.getPage(
            'http://www.google.com/ig/api?weather=%s' % str(self.city),
            method = 'GET')
        deff.addCallback(self._received_respond)
        deff.addErrback(self._received_error)
        return self.result
            
    def _received_error(self, failure):
        self.result.errback(GoogleException(failure))

    def _getData(self, nodelist, tag):
        return nodelist.getElementsByTagName(tag)[0].getAttribute('data')
            
    def _received_respond(self, respond):
        xml = parseString(respond)
        weather_info = xml.getElementsByTagName('weather')[0]
        if weather_info.getElementsByTagName('problem_cause'):
            self.result.errback(UnknownCityException('unknown city'))
            return           
        nodelist = weather_info.getElementsByTagName('current_conditions')[0]
        structure = ('condition','temp_f', 'temp_c', 'humidity',
                     'wind_condition')
        condition = {}
        for tag in structure:
            condition[tag] = self._getData(nodelist, tag)
        self.result.callback(condition)
        
        
def Res(x):
    print x

if __name__ == '__main__':
    condition1 = Weather('omsk')
    condition1 = condition1.get_weather()
    condition1.addCallback(Res)        
    reactor.run()
    
