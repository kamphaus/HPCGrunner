import copy


def filterRemaining(remaining, environment):
    returned = copy.copy(remaining)
    for r in returned:
        if any(not(r[e]==environment[e]) for e in environment if e in r):
            returned.remove(r)
        else:
            r['runs'] = copy.copy(r['runs'])
            for i in r['runs']:
                if any(not(i[e]==environment[e]) for e in environment):
                    r['runs'].remove(i)
            if len(r['runs'])==0:
                returned.remove(r)
    return returned
