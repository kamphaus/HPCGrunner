class Run(dict):
    attributes = ('nx', 'ny', 'nz', 'time', 'NbrOfCores', 'platform', 'repetitions')
    def __init__(self, serie, data):
        self.data = data
        self.parent = serie
        for x in Run.attributes:
            if x in data:
                self[x] = data[x]
            else:
                self[x] = serie[x]
#        if 'repetitions' not in self:
#            self.repetitions = 1
    
    def getReduced(self):
        return { k:self[k] for k in Run.attributes if k in self and (k not in self.serie or self[k] != self.serie[k]) }
    
    # Compare based on the attributes named in Run.attributes
    def __eq__(self, other):
        a = { k:self[k] for k in Run.attributes if k in self }
        b = { k:other[k] for k in Run.attributes if k in other }
        return a == b
