import os
from FileUtils import moveFilesOfType, findFileOfType
import ResultValidator
import timeit

class Executor(object):
    def __init__ (self, config):
        self.config = config
        if 'HPCGdir' not in self.config:
            self.config['HPCGdir'] = '.'
        self.observers = []

    def registerObserver(self, observer):
        self.observers.append(observer)

    def run(self, next):
        # TODO: Implement this
        pass

    def execute(self, next):
        print "Executing a run:"
        print "next:", next
        initial_dir = os.getcwd()
        os.chdir(self.config['HPCGdir'])
        try:
            os.chdir(next['configuration'])
            os.chdir('bin')
            fp = open("xhpcg")
            fp.close()
        except OSError as e:
            raise EnvironmentError("The configuration '"+next['configuration']+"' does not seem to exist or is not compiled properly.")
        except IOError as e:
            raise EnvironmentError("The configuration '"+next['configuration']+"' is not compiled properly or you do not have access rights.")
        if not os.path.exists('results'):
            os.mkdir('results')
        # TODO: uncomment this
        #moveFilesOfType('.', 'results', ('.txt', '.yml', '.yaml', '.log'))

        # Time execution
        start_time = timeit.default_timer()
        self.run(next)
        elapsed = timeit.default_timer() - start_time
        resultFile = findFileOfType('.', ['.yaml'])
        if resultFile is None:
            raise StandardError('The results are not available')
        result = ResultValidator.read(resultFile)
        os.chdir(initial_dir)

        # Debug output
        # TODO: fix this
        # next['results'].append(0.1)
        # next['result_id'].append(2)
        next['result_exectime'].append(0.3)
        # next['result_valid'].append(False)
        next['totalExecTime'] += 0.3
        next['results'].append(result['results'])
        next['result_id'].append(result['result_id'])
        # next['result_exectime'].append(elapsed)
        next['result_valid'].append(result['result_valid'])
        # next['totalExecTime'] += elapsed

        for o in self.observers:
            o.onUpdate(next)

