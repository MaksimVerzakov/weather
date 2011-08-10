from twisted.internet import task
from twisted.internet import defer

from weather import Weather


class WeatherBase(object):
    
    def __init__(self):
        self.cities = {}
        self.conditions = {}
        self.lc = task.LoopingCall(self.update)
        self.lc.start(150)

    def _add_city(self, city):
        self.cities[city] = Weather(city)
        weather = self.cities[city].get_weather()
        weather.addCallback(self._received_condition, city)
        weather.addErrback(self._received_error, city)        
    
    def _received_condition(self, condition, city):
        self.conditions[city] = condition
    
    def _received_error(self, failure, city):
        print 'error %s' % failure
    
    def get_condition(self, city):
        print city
        d = defer.Deferred()
        if city in self.conditions.keys():            
            d.callback(self.conditions[city])            
        else:
            self._add_city(city)
            d = Weather(city).get_weather()
        return d
        
    def update(self):
        for city in self.cities:
            self.cities[city].get_weather().addCallback(_received_condition, city)
