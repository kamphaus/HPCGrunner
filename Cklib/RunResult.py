
import Run

class RunResult(Run.Run):
    attributes = ('nx', 'ny', 'nz', 'time', 'NbrOfCores', 'platform', 'repetitions', 'results', 'result_id', 'result_exectime', 'result_valid', 'totalExecTime')
    attributesRunResult = ('results', 'result_id', 'result_exectime', 'result_valid', 'totalExecTime')
    def __init__(self, serie, data):
        Run.__init__(serie, data)
        for x in RunResult.attributesRunResult:
            if x in data:
                self[x] = data[x]
            else:
                self[x] = []
    
    def getReduced(self):
        return { k:self[k] for k in RunResult.attributes if k in self and (k not in self.serie or self[k] != self.serie[k]) }
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            a = { k:self[k] for k in RunResult.attributes if k in self }
            b = { k:other[k] for k in RunResult.attributes if k in other }
            return a == b
        else:
            return Run.__eq__(self, other)
