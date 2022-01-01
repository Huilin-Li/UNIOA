import numpy as np
from GenericFramework.NatureOpt import NatureOpt


# -------------------------------------------------------------------------------------------
# The file is a translation of Butterfly-Optimizer\cite{1,2} from MatLab to Python.
# This Python version code suits our specific experiment cases in IOHanalyzer\cite{3}.
# The execute logic is same as the original implementation in \cite{2}.
# -------------------------------------------------------------------------------------------
# References:
# [1]S. Arora and S. Singh, ‘Butterfly optimization algorithm: a novel approach for global optimization’, Soft Comput, vol. 23, no. 3, pp. 715–734, Feb. 2019, doi: 10.1007/s00500-018-3102-4.
# [2]https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/b4a529ac-c709-4752-8ae1-1d172b8968fc/67a434dc-8224-4f4e-a835-bc92c4630a73/previews/BOA.m/index.html
# [3]C. Doerr, H. Wang, F. Ye, S. van Rijn, and T. Bäck, ‘IOHprofiler: A Benchmarking and Profiling Tool for Iterative Optimization Heuristics’, arXiv:1810.05281 [cs], Oct. 2018, Accessed: Sep. 19, 2021. [Online]. Available: http://arxiv.org/abs/1810.05281
# -------------------------------------------------------------------------------------------


class raw_BOA_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor = 1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 50)
        self.prob_switch = hyperparams_set.get('probability_switch', 0.8)
        self.power_exponent = hyperparams_set.get('power_exponent', 0.1) #= a/alpha
        self.initial_sensory_modality = hyperparams_set.get('initial_sensory_modality', 0.01)# =c
        
        
    def sensory_modality_NEW(self, x, Ngen):
        return x+(0.025/(x*Ngen))

    def __call__(self):
        # initialization part
        Sol = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        fitness = self.Evaluate_X(X = Sol)
        # find the global best
        ind = np.argmin(fitness)
        best_pos= Sol[ind]
        fmin = fitness[ind]
        S=Sol.copy()
              
        sensory_modality = self.initial_sensory_modality
        while not self.stop:
            for i in range(self.M):
                FP= sensory_modality*(fitness[i]**self.power_exponent)
                if np.random.rand()>self.prob_switch:
                    dis = np.random.rand()**2*best_pos - Sol[i]
                    x=Sol[i]+dis*FP
                else:
                    epsilon=np.random.rand()
                    JK = np.random.choice(self.M, 2, replace=False)
                    dis=epsilon**2*Sol[JK[0]]-Sol[JK[1]]
                    x=Sol[i]+dis*FP  #Eq. (3) in paper
                   
                #Check if the simple limits/bounds are OK
                x = np.clip(x, self.lb_x, self.ub_x)
                  
                # Evaluate new solutions
                Fnew = self.fitness_function(x) #Fnew represents new fitness values
                    
                # If fitness improves (better solutions found), update then = selection
                if Fnew <= fitness[i]:
                    S[i] = x
                    fitness[i] = Fnew


                #Fnew = self.fitness_function(S[i])

                # Update the current global best_pos
                if Fnew<=fmin:
                    best_pos=x
                    fmin=Fnew

        
            #Update sensory_modality
            sensory_modality=self.sensory_modality_NEW(sensory_modality, Ngen=self.budget)

              
    
            
        
        
        

        
    