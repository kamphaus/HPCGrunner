
import Serie
import SerieResult

class Scheduler(object):
    def __init__(self, config, environment, results):
        self.config = config
        self.environment = environment
        self.dataResults = results
        self.previousResults = results
        self.series = ( Serie.Serie(x) for x in config['series'] )
        for p in self.series: print p
        self.results = [ SerieResult.SerieResult(x) for x in results ]
        for r in self.results: print r
        #self.test = results.nonex
        self.finishedSeries = False
        self.next = self.getNext()
    
    def hasNext(self):
        return self.next != ''
    
    def executeNext(self):
        if self.hasNext():
            return 1
    
    def getNext(self):
        return ''
    
    def getResults(self):
        return self.results
    
    def hasFinishedSeries(self):
        # There is a series that is finished that was not finished before the last execution
        return 1
    
    def getFinishedSeries(self):
        return {}
    
    def getRemaining(self):
        series = self.series
        results = self.results
        result = []
        oSeries = results.copy()
        for s in series:
            found = False
            for t in oSeries:
                if s==t:
                    found = True
                    toAdd = s.getRemaining(t)
                    # Check if there are any iterations remaining in that run
                    if len(t['results']) < t['repetitions']:
                        t['remaining'] = t['repetitions'] - len(t['results'])
                        result.append( t )
                    # Remove from oSeries
                    oSeries.remove(t)
                    break
            if not found:
                toAdd = s.getRemaining(SerieResult.SerieResult(s.data))
                result.append( toAdd )
        return result
