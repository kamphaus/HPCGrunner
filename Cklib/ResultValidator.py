from FileUtils import read_yaml_file


def validate(result):
    Spectral = result['Spectral Convergence Tests']['Result']=='PASSED'
    Symmetry = result['Departure from Symmetry |x\'Ay-y\'Ax|/(2*||x||*||A||*||y||)/epsilon']['Result']=='PASSED'
    Iteration = result['Iteration Count Information']['Result']=='PASSED'
    Reproducibility = result['Reproducibility Information']['Result']=='PASSED'
    return all((Spectral, Symmetry, Iteration, Reproducibility))

def read(file):
    result = read_yaml_file(file, fixCorruption=True)
    score = result['__________ Final Summary __________']['HPCG result is VALID with a GFLOP/s rating of']
    isValid = validate(result)
    toReturn = {
        'results':score,
        'result_id':file,
        'result_valid':isValid
    }
    return toReturn