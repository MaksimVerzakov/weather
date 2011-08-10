class SubscribedList(object):
    def __init__(self, filename):
        self.filename = filename
        self.subscr_list = []
        self.read_subscribed_list()
        
    def read_subscribed_list(self):
        subscr = open(self.filename) 
        for line in subscr.readlines():
            line = line.strip()
            k, v = line.split(' ', 1)
            self.subscr_list.append((k, v))
        subscr.close()
        return self.subscr_list
        
    def add_subscr(self, from_, to):
        if (from_, to) in self.subscr_list:
            return
        self.subscr_list.append((from_, to))
        subscr = open(self.filename, 'a')
        subscr.write('%s %s\n' %(from_, to))
        subscr.close()
    
    def rm_subscr(self, from_, to):
        self.subscr_list.remove((from_, to))
        subscr = open(self.filename, 'w')
        for from_, to in self.subscr_list:
            subscr.write('%s %s\n' %(from_, to))
        subscr.close()