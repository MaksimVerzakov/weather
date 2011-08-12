from twilix.vcard import MyVCardQuery
from twilix.stanzas import Iq
from twilix.version import MyVersionQuery

class MyIq(Iq):
    pass

class WeatherVCardQuery(MyVCardQuery):
    parentClass = Iq
    pass
      
class WeatherVersionQuery(MyVersionQuery):
    parentClass = MyIq
    pass

    
