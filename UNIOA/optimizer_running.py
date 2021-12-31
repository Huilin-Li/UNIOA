import time
import ioh
from datetime import datetime
from .algs import *
import sys, os
import importlib
from pydoc import locate
# my_class = locate('my_package.my_module.MyClass')

def optimizer_running(problems, instances, dimensions, num_runs, paras_set, optimizer_name):
    t = 0
    optimizer_name_temp = optimizer_name
    UNIOA_algs = ['BA_Opt', 'CSA_Opt', 'MFO_Opt', 'PSO_Opt', 'GOA_Opt', 'MBO_Opt', 'BOA_Opt']
    if optimizer_name not in UNIOA_algs:
        t = 1
        file_name = os.path.basename(sys.argv[0])[:-2]
        your_optimizer_name = locate(file_name + optimizer_name)
        # file_name = os.path.basename(sys.argv[0])[:-3]
        # importlib.import_module(file_name + optimizer_name)

    folder_name = optimizer_name_temp + '_folder'
    data_name = optimizer_name_temp
    st = time.time()
    print('----- ' + optimizer_name_temp + ' is optmizting your problem -----', flush=True)
    logger = ioh.logger.Analyzer(folder_name='DataFiles/'+folder_name+'/'+data_name, algorithm_name=optimizer_name_temp)
    for p_id in problems:
        print('P-id={}'.format(p_id), end=":", flush=True)
        for d in dimensions:
            print('d-{}'.format(d), end=":", flush=True)
            for i_id in instances:
                print('{}'.format(i_id), end="", flush=True)
                func = ioh.get_problem(fid=p_id, dim=d, iid=i_id)
                # func.attach_logger(logger)
                print('', end='(', flush=True)
                for rep in range(num_runs):
                    func.attach_logger(logger)
                    print('{}'.format(rep), end="", flush=True)
                    if t == 1 :
                        opt = your_optimizer_name(func, paras_set)
                    else:
                        opt = eval(optimizer_name)(func, paras_set)
                    opt()
                    func.reset()
                print('', end=')', flush=True)


    print('costs', round((time.time() - st) / 60, 2), 'minutes')
    with open("DataFiles/runningtime.txt", "a+") as text_file:
        date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        runningtime = round((time.time() - st) / 60, 2)
        print("{} | {}: {} minutes.".format(date, optimizer_name, runningtime), file=text_file)


