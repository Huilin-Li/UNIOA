from .optimizer_running import optimizer_running
import sys,os


def comparing (Algs, problems, instances, dimensions, num_runs, paras_set):
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
    paras_set = paras_set

    for alg in Algs:
        optimizer_name = alg
        optimizer_running(problems, instances, dimensions, num_runs, paras_set, optimizer_name)


