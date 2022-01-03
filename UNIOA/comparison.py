from .optimizer_running import optimizer_running



def comparing (Algs, problems, instances, dimensions, num_runs, paras_sets):
    '''
    Algs: a list of strings
    problems: a list of integers
    instances: a list of integers
    dimensions: a list of integers
    num_runs: one integer
    paras_set: dictionary
    '''
    problems = problems
    instances = instances
    dimensions = dimensions
    num_runs = num_runs

    for alg in Algs:
        optimizer_name = alg
        paras_set = paras_sets[alg]
        optimizer_running(problems, instances, dimensions, num_runs, paras_set, optimizer_name)


