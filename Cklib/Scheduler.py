
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
        self.series = list( Serie.Serie(x) for x in config['series'] )
        if all(x is None for x in results): results = ()
        self.results = list([ SerieResult.SerieResult(x) for x in results ])
        self.remaining = Diff.getRemaining(self.series, self.results)
        self.remainingExecutable = Filter.filterRemaining(self.remaining, environment)
        self.finishedSeries = None
        self.next = self.getNext()
        self.nextExecutable = self.getNextExecutable()
        #print self

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
        return self.next is not None

    def hasNextExecutable(self):
        return self.nextExecutable is not None

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

    def getResults(self):
        return self.results

    def hasFinishedSeries(self):
        """There is a series that is finished that was not finished before the last execution"""
        return self.finishedSeries is not None

    def getFinishedSeries(self):
        """Get the serie that was finished in the last execution"""
        return self.finishedSeries['result']

    def getRemaining(self):
        return self.remaining

    def getRemainingExecutable(self):
        return self.remainingExecutable

    def onUpdate(self, result):
        if result['parentRemaining']['inResult']:
            if result['inResult']:
                pass # is already updated
            else:
                result['parentRemaining']['result']['runs'].append(result)
        else:
            self.results.append(result['parentRemaining'])
            result['parentRemaining']['runs'] = [result]
        lastRemaining = self.remaining
        self.remaining = Diff.getRemaining(self.series, self.results)
        self.remainingExecutable = Filter.filterRemaining(self.remaining, self.environment)
        if len(lastRemaining) > len(self.remaining):
            self.finishedSeries = result['parentRemaining']
        else:
            self.finishedSeries = None
        self.next = self.getNext()
        self.nextExecutable = self.getNextExecutable()

