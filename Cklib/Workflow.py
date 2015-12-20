
import yaml
import Scheduler
import Executor
import Graph
import Diff

class Workflow(object):

    def execute(self):
        config = read_yaml_file('config.yml')
        print yaml.dump(config)
        envir = read_yaml_file('environment.yml')
        print yaml.dump(envir)
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        executor = Executor.Executor(config)
        executor.registerObserver(scheduler)
        graph = Graph.Graph()
        while scheduler.hasNextExecutable():
            executor.execute(scheduler.getNextExecutable())
            results = list(r.getReduced() for r in scheduler.getResults())
            save_yaml_file('results.yml', results)
            if scheduler.hasFinishedSeries():
                graph.draw(scheduler.getFinishedSeries())

    def viz(self):
        config = read_yaml_file('config.yml')
        print yaml.dump(config)
        envir = read_yaml_file('environment.yml')
        print yaml.dump(envir)
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        graph = Graph.Graph()
        results = scheduler.getResults()
        remaining = scheduler.getRemaining()
        for r in results:
            if not Diff.hasRemainingSerie(r, remaining):
                graph.draw(r)

def read_yaml_file(filename, default=None, ignoreNonExistantFile=False):
    if filename[-5:] == ".yaml" or filename[-4:] == ".yml":
        if ignoreNonExistantFile:
            try:
                file = open(filename)
                result = yaml.safe_load(file.read())
                file.close()
            except IOError:
                return default
        else:
            file = open(filename)
            result = yaml.safe_load(file.read())
            file.close()
        return result
    else:
        raise ValueError('Filename must have .yaml ending')

def save_yaml_file(filename, data):
    if filename[-5:] == ".yaml" or filename[-4:] == ".yml":
        file = open(filename, "w")
        yaml.dump(data, file)
        file.close()
    else:
        raise ValueError('Filename must have .yaml ending')

def execute(arguments):
    if 'run' in arguments.action:
        return Workflow().execute()
    if 'clean' in arguments.action:
        raise NotImplementedError('Option clean not yet implemented!')
    if 'viz' in arguments.action:
        return Workflow().viz()