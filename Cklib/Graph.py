import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import re


class Graph(object):

    def __init__(self, config=None):
        self.config = config

    def isNumberSerie(self, values):
        return all([isinstance(v, (int, long, float)) for v in values])

    def draw(self, serie):
        print "Drawing diagram"
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
            print values_param2
        values_param1 = sorted(list(set(r[param1] for r in serie['runs'])))
        print values_param1
        if param2 is None:
            series = [[[r['results'] for r in serie['runs'] if r[param1]==p] for p in values_param1]]
        else:
            series = [[[r['results'] for r in serie['runs'] if r[param1]==p and r[param2]==p2] for p in values_param1] for p2 in values_param2]
        # Flatten the inner most 2 lists: list of runs with same param1 & param2 containing list of results
        series = [[[x for z in y for x in z] for y in s] for s in series]
        print series
        calc_err = list(any(len(r)>1 for r in s) for s in series)
        print calc_err
        means = [[np.mean(x) for x in s] for s in series]
        print means
        errors = [list(np.std(x) for x in s) for s in series]
        print errors
        numDataSets = len(means)
        numXAxis = len(values_param1)

        # Create plot with data in means and errors
        fig, ax = plt.subplots()
        ax.set_title(serie['name'])
        ax.set_ylabel('HPCG result (GFLOP/s)')
        ax.set_xlabel(param1)
        if self.isNumberSerie(values_param1):
            # Use an errorbar plot
            sets = []
            for i, s in enumerate(means):
                if calc_err[i]:
                    sets.append(ax.errorbar(values_param1, s, yerr=errors[i], fmt='-o'))
                else:
                    sets.append(ax.errorbar(values_param1, s, fmt='-o'))
            if param2 is not None:
                ax.legend(sets, values_param2)
            # plt.show()
        else:
            # Use a bar plot
            ind = np.arange(numXAxis)
            width = 1.0/(numDataSets+1)
            bars = []
            for i, s in enumerate(means):
                if calc_err[i]:
                    bars.append(ax.bar(ind, s, width, yerr=errors[i]))
                else:
                    bars.append(ax.bar(ind+i*width, s, width))
            ax.set_xticks(ind + width*numDataSets/2)
            ax.set_xticklabels(values_param1)
            if param2 is not None:
                ax.legend(bars, values_param2)
            # plt.show()

        initial_dir = os.getcwd()
        os.chdir(self.config['outDir'])
        dt = datetime.datetime.now()
        plt.savefig(re.sub('[:]', '', dt.isoformat())+'.png', bbox_inches='tight')
        os.chdir(initial_dir)

        return 1
