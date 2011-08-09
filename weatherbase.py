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
        weather.addCallback(self._recived_condition, city)
        weather.addErrback(self._recived_error, city)        
    
    def _recived_condition(self, condition, city):
        self.conditions[city] = condition
    
    def _recived_error(self, condition, city):
        del self.cities[city]
    
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
            self.cities[city].get_weather().addCallback(_recived_condition, city)   
