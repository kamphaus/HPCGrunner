
class Executor(object):
    def __init__ (self, config):
        self.config = config
        self.observers = []

    def registerObserver(self, observer):
        self.observers.append(observer)

    def check(self):
        pass

    def clean(self):
        pass

    def getResult(self):
        pass

    def archive(self):
        pass

    def run(self, next):
        pass

    def execute(self, next):
        print "AHAHAHAHAH"
        print "next:", next
        next['results'].append(0.1)
        next['result_id'].append(2)
        next['result_exectime'].append(0.3)
        next['result_valid'].append(False)
        next['totalExecTime'] += 0.3
        for o in self.observers:
            o.onUpdate(next)

