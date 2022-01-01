import math
import numpy as np
from GenericFramework.NatureOpt import NatureOpt


# -------------------------------------------------------------------------------------------
# The file is a translation of Bat-Optimizer\cite{1,2} from MatLab to Python.
# This Python version code suits our specific experiment cases in IOHanalyzer\cite{3}.
# The execution logic is same as the original implementation in \cite{2}.
# -------------------------------------------------------------------------------------------
# References:
# [1]X.-S. Yang, ‘A New Metaheuristic Bat-Inspired Algorithm’, arXiv:1004.4170 [physics], Apr. 2010, Accessed: Jun. 11, 2021. [Online]. Available: http://arxiv.org/abs/1004.4170
# [2]https://uk.mathworks.com/matlabcentral/fileexchange/74768-the-standard-bat-algorithm-ba?s_tid=prof_contriblnk
# [3]C. Doerr, H. Wang, F. Ye, S. van Rijn, and T. Bäck, ‘IOHprofiler: A Benchmarking and Profiling Tool for Iterative Optimization Heuristics’, arXiv:1810.05281 [cs], Oct. 2018, Accessed: Sep. 19, 2021. [Online]. Available: http://arxiv.org/abs/1810.05281
# -------------------------------------------------------------------------------------------


class raw_BA_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor = 1e4):
        super().__init__(func,budget_factor)
        self.M = hyperparams_set.get('popsize', 20) #
        self.A = hyperparams_set.get('loudness', 1) # initial loudness A
        self.r0 = hyperparams_set.get('pulse_rate', 1) # initial pulse rate r0
        self.alpha = hyperparams_set.get('alpha', 0.97) # to decrease A
        self.gamma = hyperparams_set.get('gamma', 0.1) # to decrease r0
        self.Freq_min = hyperparams_set.get('frequency_min', 0)
        self.Freq_max = hyperparams_set.get('frequency_max', 2)
        
    def __call__(self):
        v = np.zeros((self.M, self.n))  # Velocities

        # Initialize the population/solutions
        Sol = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        Fitness = self.Evaluate_X(X = Sol)

        # Find the best solution of the initial population
        I = np.argmin(Fitness)
        best = Sol[I]
        fmin = min(Fitness)

        # iteration counter
        t = 0
        A=self.alpha*self.A
        # Start the iterations -- the Bat Algorithm (BA) -- main loop
        while not self.stop:
            #  Varying loundness (A) and pulse emission rate (r)
            r=self.r0*(1-math.exp(-self.gamma*t))
            # Loop over all bats/solutions
            S = Sol.copy()
            #SS = S.copy()
            for i in range(self.M):
                Freq=self.Freq_min+(self.Freq_max-self.Freq_min)*np.random.rand()
                v[i]=v[i]+(Sol[i]-best)*Freq
                x= Sol[i] + v[i]
                # Check a switching condition
                if np.random.rand()<r:
                    x= best + 0.1 * np.random.randn(self.n) * A
                # Check if the new solution is within the simple bounds
                x = np.clip(x, self.lb_x, self.ub_x)
                #SS[i] = x

                # Evaluate new solution
                Fnew_temp = self.fitness_function(x)
                # If the solution improves or not too loudness= selection
                if ((Fnew_temp<=Fitness[i]) and (np.random.rand()>A)):
                    S[i] = x # final new generated pop
                Fitness[i] = self.fitness_function(S[i])
                
               # Update the current best solution
                if Fitness[i]<=fmin:
                   best=S[i]
                   fmin=Fitness[i]
                   
            t=t+1
            A = self.alpha*A
            Sol = S
