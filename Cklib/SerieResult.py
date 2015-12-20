
import Serie
import RunResult


class SerieResult(Serie.Serie):

    def init(self, data):
        self['runs'] = list([ RunResult.RunResult(self, d) for d in data['runs'] ])
        pass