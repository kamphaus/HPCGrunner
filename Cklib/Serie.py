import Run


class Serie(dict):
    attributes = (
        'name', 'nx', 'ny', 'nz', 'time', 'NbrOfCores', 'platform', 'configuration', 'repetitions', 'mpiargs',
        'abbrv', 'viz')

    def __init__(self, data, **kwargs):
        super(Serie, self).__init__(**kwargs)
        self.data = data
        for x in Serie.attributes:
            if x in data:
                self[x] = data[x]
        self['runs'] = list(Run.Run(self, d) for d in data['runs'])
        if hasattr(self, 'init'):
            self.init(data)

    def getReduced(self):
        result = {k: self[k] for k in Serie.attributes if k in self}
        result['runs'] = list(run.getReduced() for run in self['runs'])
        return result

    # Compare based on the attributes named in Serie.attributes
    def __eq__(self, other):
        if isinstance(other, Serie):
            a = {k: self[k] for k in Serie.attributes if k in self}
            b = {k: other[k] for k in Serie.attributes if k in other}
            return a == b
        else:
            return super(Serie, self).__eq__(other)
