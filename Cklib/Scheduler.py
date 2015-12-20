
import Serie
import SerieResult
import Diff
import Filter

class Scheduler(object):
    def __init__(self, config, environment, results):
        self.config = config
        self.environment = environment
        self.dataResults = results
        self.previousResults = results
        print
        print "config['series']=",config['series']
        for s in config['series']:
            print s
        print
        self.series = list( Serie.Serie(x) for x in config['series'] )
        for p in self.series: print p
        print "2th:"
        for p in self.series: print p
        print
        self.results = list([ SerieResult.SerieResult(x) for x in results ])
        for r in self.results: print r
        print
        #self.test = results.nonex
        self.remaining = Diff.getRemaining(self.series, self.results)
        self.remainingExecutable = Filter.filterRemaining(self.remaining, environment)
        self.finishedSeries = False
        self.next = self.getNext()
        self.nextExecutable = self.getNextExecutable()
        print self

    def __str__(self):
        return "Scheduler obj: {\n\
            config: " + str(self.config) + "\n\
            environment: " + str(self.environment) + "\n\
            dataResults: " + str(self.dataResults) + "\n\
            previousResults: " + str(self.previousResults) + "\n\
            series: " + str(self.series) + "\n\
            results: " + str(self.results) + "\n\
            remaining: " + str(self.remaining) + "\n\
            remainingExecutable: " + str(self.remainingExecutable) + "\n\
            finishedSeries: " + str(self.finishedSeries) + "\n\
            next: " + str(self.next) + "\n\
            nextExecutable: " + str(self.nextExecutable) + "\n\
        }"

    def hasNext(self):
        #return self.next is not None
        return False

    def hasNextExecutable(self):
        #return self.nextExecutable is not None
        return False

    def getNext(self):
        for s in self.remaining:
            for r in s['runs']:
                return r
        return None

    def getNextExecutable(self):
        for s in self.remainingExecutable:
            for r in s['runs']:
                return r
        return None

    def executeNext(self):
        if self.hasNextExecutable():
            return 1

    def getResults(self):
        return self.results

    def hasFinishedSeries(self):
        """There is a series that is finished that was not finished before the last execution"""
        return 1

    def getFinishedSeries(self):
        return {}
