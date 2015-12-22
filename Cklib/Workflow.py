import Scheduler
import Executor
import Counter
import Graph
import Diff
from FileUtils import read_yaml_file, save_yaml_file, archiveFile
import os


class Workflow(object):
    def execute(self):
        config = read_yaml_file('config.yml')
        envir = read_yaml_file('environment.yml')
        initial_dir = os.getcwd()
        os.chdir(config['outDir'])
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        os.chdir(initial_dir)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        executor = Executor.Executor(config)
        executor.registerObserver(scheduler)
        graph = Graph.Graph(config)
        while scheduler.hasNextExecutable():
            print "Remaining total time:", Counter.countRemaining(scheduler.getRemaining())
            print "Remaining time:", Counter.countRemaining(scheduler.getRemainingExecutable())
            executor.execute(scheduler.getNextExecutable())
            results = list(r.getReduced() for r in scheduler.getResults())
            os.chdir(config['outDir'])
            save_yaml_file('results.yml', results)
            os.chdir(initial_dir)
            if scheduler.hasFinishedSeries():
                graph.draw(scheduler.getFinishedSeries())

    def viz(self):
        config = read_yaml_file('config.yml')
        envir = read_yaml_file('environment.yml')
        initial_dir = os.getcwd()
        os.chdir(config['outDir'])
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        os.chdir(initial_dir)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        graph = Graph.Graph(config)
        results = scheduler.getResults()
        remaining = scheduler.getRemaining()
        for r in results:
            if not Diff.hasRemainingSerie(r, remaining):
                graph.draw(r)

    def clean(self):
        config = read_yaml_file('config.yml')
        initial_dir = os.getcwd()
        os.chdir(config['outDir'])
        archiveFile('results.yml')
        os.chdir(initial_dir)

def execute(arguments):
    if 'run' in arguments.action:
        return Workflow().execute()
    if 'viz' in arguments.action:
        return Workflow().viz()
    if 'clean' in arguments.action:
        Workflow().clean()
