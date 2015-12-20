
import Serie
import RunResult


class SerieResult(Serie.Serie):

    def __init__(self, data):
        Serie.Serie.__init__(self, data)

    def init(self, data):
        self['runs'] = list([ RunResult.RunResult(self, d) for d in data['runs'] ])
