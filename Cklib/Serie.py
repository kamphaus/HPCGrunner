
import Run

class Serie(dict):
    attributes = ('name', 'nx', 'ny', 'nz', 'time', 'NbrOfCores', 'platform', 'repetitions', 'viz')
    def __init__(self, data):
        self.data = data
        for x in Serie.attributes:
            if x in data:
                self[x] = data[x]
        self['runs'] = ( Run.Run(self, d) for d in data['runs'] )
    
    def getReduced(self):
        result = self.copy()
        result['runs'] = ( run.getReduced() for run in self['runs'] )
        return result
    
    def getRemaining(self, other):
        if not self==other:
            raise ValueError('To get the remaining runs the attribute\'s Serie and SerieResult must match')
        result = []
        oRuns = other['runs'].copy()
        for r in self['runs']:
            found = False
            for t in oRuns:
                if r==t:
                    found = True
                    # Check if there are any iterations remaining in that run
                    if len(t['results']) < t['repetitions']:
                        t['remaining'] = t['repetitions'] - len(t['results'])
                        result.append( t )
                    # Remove from oRuns
                    oRuns.remove(t)
                    break
            if not found:
                toAdd = RunResult.RunResult(r.data)
                toAdd['remaining'] = toAdd['repetitions']
                result.append( toAdd )
        return result
    
    # Compare based on the attributes named in Serie.attributes
    def __eq__(self, other):
        a = { k:self[k] for k in Serie.attributes if k in self }
        b = { k:other[k] for k in Serie.attributes if k in other }
        return a == b
