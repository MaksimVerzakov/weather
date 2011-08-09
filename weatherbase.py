from twisted.internet import reactor, task
from twisted.internet import defer

from weather import Weather


class WeatherBase(object):
    
    def __init__(self):
        self.cities = {}
        self.conditions = {}

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
            

def Res(x, city):
    print '%s : %s' % (city, x)

def temp(wb):
    omsk2 = wb.get_condition('omsk')
    omsk2.addCallback(Res, 'omsk2')

if __name__ == '__main__':
    wb = WeatherBase()
    omsk = wb.get_condition('omsk')
    omsk.addCallback(Res, 'omsk1')
    kiev = wb.get_condition('kiev')
    kiev.addCallback(Res, 'kiev')
    reactor.callLater(4, temp, wb)
    reactor.run()
        
