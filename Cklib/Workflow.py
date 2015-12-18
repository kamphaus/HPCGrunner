
import yaml
import Scheduler
import Graph

class Workflow(object):

    def execute(self):
        config = read_yaml_file('config.yml')
        print yaml.dump(config)
        envir = read_yaml_file('environment.yml')
        print yaml.dump(envir)
        results = read_yaml_file('results.yml', default=(), ignoreNonExistantFile=True)
        scheduler = Scheduler.Scheduler(config, envir, results)
        graph = Graph.Graph()
        while scheduler.hasNext():
            scheduler.executeNext()
            results = scheduler.getResults()
            save_yaml_file('results.yml', results)
            if scheduler.hasFinishedSeries():
                graph.draw(scheduler.getFinishedSeries())
    
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

def execute():
    return Workflow().execute()