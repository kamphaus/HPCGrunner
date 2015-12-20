def countRemaining(series):
    secs = 0
    for s in series:
        for r in s['runs']:
            if 'remaining' in r:
                secs += r['remaining']*r['time']
            else:
                secs += r['repetitions']*r['time']
    return secs