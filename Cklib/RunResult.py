
import Run

class RunResult(Run.Run):
    attributes = ('nx', 'ny', 'nz', 'time', 'NbrOfCores', 'platform', 'configuration', 'repetitions', 'mpiargs', 'results', 'result_id', 'result_exectime', 'result_valid', 'totalExecTime')
    attributesRunResult = ('results', 'result_id', 'result_exectime', 'result_valid', 'totalExecTime')

    def __init__(self, serie, data):
        Run.Run.__init__(self, serie, data)

    def init(self, serie, data):
        for x in RunResult.attributesRunResult:
            if x in data:
                self[x] = data[x]
            else:
                self[x] = []
        if self['totalExecTime']==[]: self['totalExecTime'] = 0.0
        #if 'results' not in self: self['results'] = []

    def getReduced(self):
        return { k:self[k] for k in RunResult.attributes if k in self and (k not in self.parent or self[k] != self.parent[k]) }
    
    def __eq__(self, other):
        if isinstance(other, self.__class__) and isinstance(self, other.__class__):
            a = { k:self[k] for k in RunResult.attributes if k in self }
            b = { k:other[k] for k in RunResult.attributes if k in other }
            return a == b
        else:
            return Run.Run.__eq__(self, other)
