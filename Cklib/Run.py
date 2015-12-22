class Run(dict):
    attributes = ('nx', 'ny', 'nz', 'time', 'NbrOfCores', 'platform', 'configuration', 'repetitions', 'mpiargs')
    def __init__(self, serie, data, **kwargs):
        super(Run, self).__init__(**kwargs)
        self.data = data
        self.parent = serie
        for x in Run.attributes:
            if x in data:
                self[x] = data[x]
            else:
                self[x] = serie[x]
#        if 'repetitions' not in self:
#            self.repetitions = 1
        #if 'results' not in self: self['results'] = []
        if hasattr(self, 'init'):
            self.init(serie, data)

    def getReduced(self):
        return { k:self[k] for k in Run.attributes if k in self and (k not in self.parent or self[k] != self.parent[k]) }
    
    # Compare based on the attributes named in Run.attributes
    def __eq__(self, other):
        if isinstance(other, Run):
            a = { k:self[k] for k in Run.attributes if k in self }
            b = { k:other[k] for k in Run.attributes if k in other }
            return a == b
        else:
            return super(Run, self).__eq__(other)
