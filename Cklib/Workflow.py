import Scheduler
import Executor
import Graph
import Diff
from FileUtils import read_yaml_file, save_yaml_file, archiveFile


class Workflow(object):
    def execute(self):
        config = read_yaml_file('config.yml')
        envir = read_yaml_file('environment.yml')
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        executor = Executor.Executor(config)
        executor.registerObserver(scheduler)
        graph = Graph.Graph(config)
        while scheduler.hasNextExecutable():
            executor.execute(scheduler.getNextExecutable())
            results = list(r.getReduced() for r in scheduler.getResults())
            save_yaml_file('results.yml', results)
            if scheduler.hasFinishedSeries():
                graph.draw(scheduler.getFinishedSeries())

    def viz(self):
        config = read_yaml_file('config.yml')
        envir = read_yaml_file('environment.yml')
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        graph = Graph.Graph(config)
        results = scheduler.getResults()
        remaining = scheduler.getRemaining()
        for r in results:
            if not Diff.hasRemainingSerie(r, remaining):
                graph.draw(r)

    def clean(self):
        archiveFile('results.yml')

def execute(arguments):
    if 'run' in arguments.action:
        return Workflow().execute()
    if 'viz' in arguments.action:
        return Workflow().viz()
    if 'clean' in arguments.action:
        Workflow().clean()
