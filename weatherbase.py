from twisted.internet import task
from twisted.internet import defer

from weather import Weather
from weather import UnknownCityException


class WeatherBase(object):
    
    def __init__(self):
        self.cities = {}
        self.conditions = {}
        self.lc = task.LoopingCall(self._update)
        self.lc.start(9)

    def _add_city(self, city):
        self.cities[city] = Weather(city)        
            
    def get_condition(self, city):
        d = defer.Deferred()
        if city in self.conditions.keys():            
            d.callback(self.conditions[city])
        else:
            self._add_city(city)
            d = Weather(city).get_weather()
        return d
        
    def _update(self):
        def upt_error(city, err):
            if isinstance(err, UnknownCityException):
                self.cities.remove(city)
        for city in self.cities:
            d = self.cities[city].get_weather()
            d.addCallback(self._received_condition, city)
            d.addErrback(upt_error, city)
    
    def _received_condition(self, condition, city):
        self.conditions[city] = condition
