import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import re


class Graph(object):

    def __init__(self, config, alert):
        self.config = config
        self.alert = alert

    @staticmethod
    def isNumberSerie(values):
        return all([isinstance(v, (int, long, float)) for v in values])

    def draw(self, serie):
        alert = self.alert
        print "Drawing diagram..."
        alert.info("Drawing diagram...")
        if self.config['verbosity']>2:
            print "for:", serie

        # Preprocessing: remove invalid test results
        if 'removeInvalid' not in serie['viz'] or serie['viz']['removeInvalid']==True:
            for r in serie['runs']:
                # Traverse in reverse order to keep indices intact when removing items
                for i, valid in reversed(list(enumerate(r['result_valid']))):
                    if not valid:
                        del r['result_exectime'][i]
                        del r['results'][i]
                        del r['result_id'][i]
                        del r['result_valid'][i]

        param1 = serie['viz']['param1']
        if 'param2' in serie['viz']:
            param2 = serie['viz']['param2']
        else:
            param2 = None
        if param2 is not None:
            values_param2 = sorted(list(set(r[param2] for r in serie['runs'])))
            if self.config['verbosity']>2:
                print values_param2
        values_param1 = sorted(list(set(r[param1] for r in serie['runs'])))
        if self.config['verbosity']>2:
            print values_param1
        if param2 is None:
            series = [[[r['results'] for r in serie['runs'] if r[param1]==p] for p in values_param1]]
        else:
            series = [[[r['results'] for r in serie['runs'] if r[param1]==p and r[param2]==p2] for p in values_param1] for p2 in values_param2]
        # Flatten the inner most 2 lists: list of runs with same param1 & param2 containing list of results
        series = [[[x for z in y for x in z] for y in s] for s in series]
        if self.config['verbosity']>2:
            print series
        calc_err = list(any(len(r)>1 for r in s) for s in series)
        if self.config['verbosity']>2:
            print calc_err
        means = [[np.mean(x) for x in s] for s in series]
        if self.config['verbosity']>2:
            print means
        errors = [list(np.std(x) for x in s) for s in series]
        if self.config['verbosity']>2:
            print errors
        numDataSets = len(means)
        numXAxis = len(values_param1)

        # Create plot with data in means and errors
        fig, ax = plt.subplots()
        ax.set_title(serie['name'])
        if 'ylabel' in serie['viz']:
            ax.set_ylabel(serie['viz']['ylabel'])
        else:
            ax.set_ylabel('HPCG result (GFLOP/s)')
        if 'xlabel' in serie['viz']:
            ax.set_xlabel(serie['viz']['xlabel'])
        else:
            ax.set_xlabel(param1)
        sets = []
        if self.isNumberSerie(values_param1):
            # Use an errorbar plot
            for i, s in enumerate(means):
                if calc_err[i]:
                    sets.append(ax.errorbar(values_param1, s, yerr=errors[i], fmt='-o'))
                else:
                    sets.append(ax.errorbar(values_param1, s, fmt='-o'))
            if param2 is not None:
                if 'legendtitle' in serie['viz']:
                    ax.legend(sets, values_param2, title=serie['viz']['legendtitle'])
                else:
                    ax.legend(sets, values_param2)
        else:
            # Use a bar plot
            ind = np.arange(numXAxis)
            width = 1.0/(numDataSets+1)
            for i, s in enumerate(means):
                if calc_err[i]:
                    sets.append(ax.bar(ind, s, width, yerr=errors[i]))
                else:
                    sets.append(ax.bar(ind+i*width, s, width))
            ax.set_xticks(ind + width*numDataSets/2)
            ax.set_xticklabels(values_param1)

        if param2 is not None:
            legendtitle = None
            loc = None
            if 'legendtitle' in serie['viz']:
                legendtitle = serie['viz']['legendtitle']
            if 'loc' in serie['viz']:
                loc = serie['viz']['loc']
            ax.legend(sets, values_param2, title=legendtitle, loc=loc)
        # plt.show()

        initial_dir = os.getcwd()
        os.chdir(self.config['outDir'])
        dt = datetime.datetime.now()
        if 'abbrv' in serie:
            plt.savefig(re.sub('[:]', '', dt.isoformat())+'-'+serie['abbrv']+'.png', bbox_inches='tight')
        else:
            plt.savefig(re.sub('[:]', '', dt.isoformat())+'.png', bbox_inches='tight')
        os.chdir(initial_dir)

        return 1
