import argparse
from set import *




parser = argparse.ArgumentParser(description='Execute Experiments on IOHanalyzer.')
parser.add_argument('-n', '--name', type=str, required=True, metavar='',
                    help='Optimizer will be executed.')
parser.add_argument('-p','--problems', type=str, default= '1:24', metavar='',
                    help='Problems used to optimize (default: from Problem-1 to Problem-24).')
parser.add_argument('-d', '--dimensions', type=str, default='5,20', metavar='',
                    help='Dimensions used to experiments (default: Dimension-5 and Dimension-20).')
parser.add_argument('-i', '--instances', type=int, default=5, metavar='',
                    help='Number of instances used to experiments (default: 5 instances).')
parser.add_argument('-r', '--runs', type=int, default=5, metavar='',
                    help='Number of experiments executed per problem per instance per dimension (default: 5 runs).')

args = parser.parse_args()

if __name__ == "__main__":
    # gather information from terminal
    optimizer_name =args.name
    p_str = args.problems
    d_str = args.dimensions
    i_int= args.instances
    r_int = args.runs

    # extract inputs
    problems = problems_option(problems_input=p_str)
    instances = instances_option(instances_input=i_int)
    dimensions = dimension_option(dimensions_input=d_str)
    num_runs = run_option(runs_input=r_int)

    paras_set = {}

    print('#######_NEW_###############################################################################')
    optimizer_running(problems, instances, dimensions, num_runs, paras_set, optimizer_name)

    # dir = optimizer_name + '_folder'
    # folder_name = os.listdir(dir)[-1]
    # os.chdir(dir)
    # shutil.make_archive(folder_name, 'zip')
    # os.rename(folder_name+'.zip', optimizer_name+'.zip')


    # name is the class name
    # raw_optimizer_names = ['raw_BA_Opt', 'raw_CSA_Opt', 'raw_MFO_Opt', 'raw_PSOOpt',
    #                        'raw_GOA_Opt', 'raw_MBO_Opt', 'raw_BOA_Opt']
    #
    # my_optimizer_names = ['BA_Opt', 'CSA_Opt', 'MFO_Opt', 'PSO_Opt',
    #                       'GOA_Opt', 'MBO_Opt', 'BOA_Opt']













     
    
    



