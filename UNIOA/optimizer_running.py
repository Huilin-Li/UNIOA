import time
import ioh
from datetime import datetime
from .algs import *
import sys, os
from pydoc import locate

# def optimizer_running(problems, instances, dimensions, num_runs, paras_set, optimizer_name, output_name):
#     Which_alg = output_name.split("_")[1]
#     folder_name = Which_alg + '_folder'
#     data_name = output_name
#     st = time.time()
#     print('--->   ' + output_name + ' is optmizting', flush=True)
#     logger = ioh.logger.Analyzer(folder_name='DataFiles/'+folder_name+'/'+data_name, algorithm_name=output_name)
#     for p_id in problems:
#         print('P-id={}'.format(p_id), end=":", flush=True)
#         for d in dimensions:
#             print('d-{}'.format(d), end=":", flush=True)
#             for i_id in instances:
#                 print('{}'.format(i_id), end="", flush=True)
#                 func = ioh.get_problem(fid=p_id, dim=d, iid=i_id)
#                 print('', end='(', flush=True)
#                 for rep in range(num_runs):
#                     #func.attach_logger(logger)
#                     print('{}'.format(rep), end="", flush=True)
#                     func.attach_logger(logger)
#                     opt = eval(optimizer_name)(func, paras_set)
#                     opt()
#                     func.reset()
#                 print('', end=')', flush=True)
#
#     print('costs', round((time.time() - st) / 60, 2), 'minutes')
#     with open("DataFiles/runningtime_" + Which_alg + ".txt", "a+") as text_file:
#         date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#         runningtime = round((time.time() - st) / 60, 2)
#         print("{} | {}: {} minutes.".format(date, output_name, runningtime), file=text_file)
#


def optimizer_running(problems, instances, dimensions, num_runs, paras_set, optimizer_name):
    t = 0
    optimizer_name_temp = optimizer_name
    UNIOA_algs = ['BA_UNIOA', 'CSA_UNIOA', 'MFO_UNIOA', 'PSO_UNIOA', 'GOA_UNIOA', 'MBO_UNIOA', 'BOA_UNIOA']
    if optimizer_name not in UNIOA_algs:
        t = 1
        file_name = os.path.basename(sys.argv[0])[:-2]
        your_optimizer_name = locate(file_name + optimizer_name)


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


