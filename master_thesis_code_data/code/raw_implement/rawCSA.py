import numpy as np
from GenericFramework.NatureOpt import NatureOpt

# -------------------------------------------------------------------------------------------
# The file is a translation of Crow-Optimizer\cite{1,2} from MatLab to Python.
# This Python version code suits our specific experiment cases in IOHanalyzer\cite{3}.
# The execution logic is same as the original implementation in \cite{2}.
# -------------------------------------------------------------------------------------------
# References:
# [1]A. Askarzadeh, ‘A novel metaheuristic method for solving constrained engineering optimization problems: Crow search algorithm’, Computers & Structures, vol. 169, pp. 1–12, Jun. 2016, doi: 10.1016/j.compstruc.2016.03.001.
# [2]https://nl.mathworks.com/matlabcentral/fileexchange/57867-crow-search-algorithm-for-constrained-optimization?focused=6496133&s_tid=gn_loc_drop&tab=function
# [3]C. Doerr, H. Wang, F. Ye, S. van Rijn, and T. Bäck, ‘IOHprofiler: A Benchmarking and Profiling Tool for Iterative Optimization Heuristics’, arXiv:1810.05281 [cs], Oct. 2018, Accessed: Sep. 19, 2021. [Online]. Available: http://arxiv.org/abs/1810.05281
# -------------------------------------------------------------------------------------------

class raw_CSA_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize',20)
        self.AP = hyperparams_set.get('awareness_probability', 0.1)
        self.fl = hyperparams_set.get('flight_length', 2)

    def __call__(self):
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        fitness = self.Evaluate_X(X = X)
        M=X.copy() # = just itself , used to get neighbors
        fit=fitness.copy()

        # update xnew , update the assistant
        Xnew = X.copy()
        while not self.stop:
            for i in range(self.M):
                if np.random.rand() > self.AP:
                    new = X[i]+self.fl*np.random.rand()*(M[np.random.randint(self.M)]-X[i])
                else:
                    new= np.random.uniform(self.lb_x, self.ub_x, self.n)
                # check position
                if np.all(new >=self.lb_x) & np.all(new <= self.ub_x):
                    Xnew[i] = new

            # evaluate fitness of assistant
            fitness_temp = self.Evaluate_X(X = Xnew)

            # selection
            for i in range(self.M):
                if fitness_temp[i] < fit[i]:
                    M[i] = Xnew[i]
                    fit[i] = fitness_temp[i]

            X = M






            
                        
                    
            

            
            
        

    
   
        
            
 