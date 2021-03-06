import copy


def filterRemaining(remaining, environment):
    returned = copy.copy(remaining)
    for i in range(len(returned)-1, -1, -1):
        r = returned[i]
        if any(not(r[e]==environment[e]) for e in environment if e in r):
            del returned[i]
        else:
            runs = copy.copy(r['runs'])
            for j in range(len(runs)-1, -1, -1):
                u = runs[j]
                if any(not(u[e]==environment[e]) for e in environment):
                    del runs[j]
            if len(runs)==0:
                del returned[i]
            else:
                r = copy.deepcopy(r)
                r['runs'] = runs
                returned[i] = r
    return returned
