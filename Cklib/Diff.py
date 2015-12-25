import SerieResult
import RunResult
import copy


def getRemainingSerie(left, right):
    if not left==right:
        raise ValueError('To get the remaining runs the attribute\'s Serie and SerieResult must match')
    result = []
    returned = SerieResult.SerieResult(left.data)
    oRuns = copy.copy(right['runs'])
    for r in left['runs']:
        found = False
        for t in oRuns:
            if r==t:
                found = True
                # Check if there are any iterations remaining in that run
                if len(t['results']) < t['repetitions']:
                    t['remaining'] = t['repetitions'] - len(t['results'])
                    t['parentRemaining'] = returned
                    t['inResult'] = True
                    result.append( t )
                # Remove from oRuns
                oRuns.remove(t)  # OK to use remove due to break
                break
        if not found:
            toAdd = RunResult.RunResult(returned, r.data)
            toAdd['remaining'] = toAdd['repetitions']
            toAdd['parentRemaining'] = returned
            toAdd['inResult'] = False
            result.append( toAdd )
    returned['runs'] = result
    return returned

def getRemaining(series, results):
    result = []
    oSeries = copy.copy(results)
    for s in series:
        found = False
        for t in oSeries:
            if s==t:
                found = True
                toAdd = getRemainingSerie(s, t)
                toAdd['inResult'] = True
                toAdd['result'] = t
                # Check if there are any iterations remaining in that run
                if len(toAdd['runs'])>0:
                    result.append( toAdd )
                # Remove from oSeries
                oSeries.remove(t)  # OK to use remove due to break
                break
        if not found:
            toAdd = getRemainingSerie(s, SerieResult.SerieResult(s.data))
            toAdd['inResult'] = False
            toAdd['result'] = toAdd
            result.append( toAdd )
    return result

def hasRemainingSerie(serie, remaining):
    for r in remaining:
        if serie==r:
            return True
    return False