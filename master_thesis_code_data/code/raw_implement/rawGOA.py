import numpy as np
from GenericFramework.NatureOpt import NatureOpt
from sklearn.metrics import pairwise_distances



# -------------------------------------------------------------------------------------------
# The file is a translation of Grasshopper-Optimizer (faster version)\cite{1,2} from MatLab to Python.
# This Python version code suits our specific experiment cases in IOHanalyzer\cite{3}.
# The execution logic is same as the original implementation in \cite{2}.
# -------------------------------------------------------------------------------------------
# References:
# [1]S. Saremi, S. Mirjalili, and A. Lewis, ‘Grasshopper Optimisation Algorithm: Theory and application’, Advances in Engineering Software, vol. 105, pp. 30–47, Mar. 2017, doi: 10.1016/j.advengsoft.2017.01.004.
# [2]https://seyedalimirjalili.com/goa
# [3]C. Doerr, H. Wang, F. Ye, S. van Rijn, and T. Bäck, ‘IOHprofiler: A Benchmarking and Profiling Tool for Iterative Optimization Heuristics’, arXiv:1810.05281 [cs], Oct. 2018, Accessed: Sep. 19, 2021. [Online]. Available: http://arxiv.org/abs/1810.05281
# -------------------------------------------------------------------------------------------


class raw_GOA_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor = 1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 100)


    def __call__(self):
        cMax=1
        cMin=0.00004
        l = 1

        # initialization
        GrassHopperPositions = np.random.uniform(self.lb_x, self.ub_x, (self.M, self.n))
        # evaluation
        GrassHopperFitness = self.Evaluate_X(X=GrassHopperPositions)

        # Find the best grasshopper (target) in the first population
        ind = np.argmin(GrassHopperFitness)
        TargetPosition = GrassHopperPositions[ind]
        TargetFitness = GrassHopperFitness[ind]
        
        # Main loop
        while not self.stop:
            c=cMax-l*((cMax-cMin)/self.budget) # Eq. (2.8) in the paper, self.budget =  Max_iter
            Dist = pairwise_distances(GrassHopperPositions, metric='euclidean')
            temp = GrassHopperPositions
            for i in range(self.M):
                S_i = np.zeros(self.n)
                for j in list(range(i)) + list(range(i+1, self.M)):
                    D=Dist[i,j]
                    r_ij_vec=(temp[i]-temp[j])/(D + 2.2204e-16) # xj-xi/dij in Eq. (2.7)
                    xj_xi=2+np.remainder(D,2) #|xjd - xid| in Eq. (2.7)
                    s_ij=((self.ub_x - self.lb_x)*c/2)*(0.5*np.exp(-xj_xi/1.5)-np.exp(-xj_xi)) *r_ij_vec # The first part inside the big bracket in Eq. (2.7)
                    S_i=S_i+s_ij

                X_new = c * S_i + TargetPosition
                # deal with outliers
                GrassHopperPositions[i] = np.clip(X_new, self.lb_x, self.ub_x)

            # evaluate new pop
            GrassHopperFitness = self.Evaluate_X(X=GrassHopperPositions)
            # no selection

            # update global best = named Target Position here
            for i in range(self.M):
                if GrassHopperFitness[i]<TargetFitness:
                    TargetPosition=GrassHopperPositions[i]
                    TargetFitness=GrassHopperFitness[i]
            l = l + 1
            
        
                
                
     
        
        
        
        
        
         
        
    