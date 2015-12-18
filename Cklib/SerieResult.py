
import Serie

class SerieResult(Serie.Serie):

    def __init__(self, data):
        Serie.__init__(data)
        self.runs = [ RunResult.RunResult(self, d) for d in data['runs'] ]
