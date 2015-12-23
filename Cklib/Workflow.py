import Scheduler
import Executor
import Counter
import Graph
import Alert
import Diff
from FileUtils import read_yaml_file, save_yaml_file, archiveFile
import os


class Workflow(object):
    def __init__(self, alert):
        self.alert = alert

    def execute(self):
        alert = self.alert
        config = read_yaml_file('config.yml')
        envir = read_yaml_file('environment.yml')
        initial_dir = os.getcwd()
        os.chdir(config['outDir'])
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        os.chdir(initial_dir)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        executor = Executor.Executor(config, alert)
        executor.registerObserver(scheduler)
        graph = Graph.Graph(config, alert)
        countAllRemaining = Counter.countRemaining(scheduler.getRemaining())
        countRemaining = Counter.countRemaining(scheduler.getRemainingExecutable())
        if countAllRemaining > countRemaining:
            alert.warn("Some runs can only be executed in another environment!")
        while scheduler.hasNextExecutable():
            countAllRemaining = Counter.countRemaining(scheduler.getRemaining())
            countRemaining = Counter.countRemaining(scheduler.getRemainingExecutable())
            message = "Remaining time: "+str(countRemaining)
            if countAllRemaining > countRemaining:
                message += " (+" + str(countAllRemaining-countRemaining) + " in another env.)"
            print message
            alert.info(message)
            executor.execute(scheduler.getNextExecutable())
            results = list(r.getReduced() for r in scheduler.getResults())
            os.chdir(config['outDir'])
            save_yaml_file('results.yml', results)
            os.chdir(initial_dir)
            if scheduler.hasFinishedSeries():
                graph.draw(scheduler.getFinishedSeries())

    def viz(self):
        alert = self.alert
        config = read_yaml_file('config.yml')
        envir = read_yaml_file('environment.yml')
        initial_dir = os.getcwd()
        os.chdir(config['outDir'])
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        os.chdir(initial_dir)
        if results is None: results = ()
        scheduler = Scheduler.Scheduler(config, envir, results)
        graph = Graph.Graph(config, alert)
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
    config = read_yaml_file('config.yml')
    a = Alert.Alert(config)
    try:
        if 'run' in arguments.action:
            Workflow(a).execute()
        if 'viz' in arguments.action:
            Workflow(a).viz()
        if 'clean' in arguments.action:
            Workflow(a).clean()
        a.ok("Finished execution!")
    except BaseException as e:
        a.error(repr(e))
        raise
