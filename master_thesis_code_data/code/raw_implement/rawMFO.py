from GenericFramework.NatureOpt import NatureOpt
import numpy as np
import math

# -------------------------------------------------------------------------------------------
# The file is a translation of MothFlame-Optimizer\cite{1,2} from MatLab to Python.
# This Python version code suits our specific experiment cases in IOHanalyzer\cite{3}.
# The execution logic is same as the original implementation in \cite{2}.
# -------------------------------------------------------------------------------------------
# References:
# [1]S. Mirjalili, ‘Moth-flame optimization algorithm: A novel nature-inspired heuristic paradigm’, Knowledge-Based Systems, vol. 89, pp. 228–249, Nov. 2015, doi: 10.1016/j.knosys.2015.07.006.
# [2]https://uk.mathworks.com/matlabcentral/fileexchange/52270-moth-flame-optimization-mfo-algorithm-toolbox?s_tid=srchtitle
# [3]C. Doerr, H. Wang, F. Ye, S. van Rijn, and T. Bäck, ‘IOHprofiler: A Benchmarking and Profiling Tool for Iterative Optimization Heuristics’, arXiv:1810.05281 [cs], Oct. 2018, Accessed: Sep. 19, 2021. [Online]. Available: http://arxiv.org/abs/1810.05281
# -------------------------------------------------------------------------------------------

class raw_MFO_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor = 1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 30)
        
    def __call__(self):
        # Initialize the positions of moths
        Moth_pos = np.random.uniform(self.lb_x, self.ub_x, (self.M, self.n))

        Iteration = 0
    
        # Main loop
        while not self.stop:
    
            # Number of flames Eq. (3.14) in the paper
            Flame_no = round(self.M - Iteration * ((self.M - 1) / self.budget))
            Moth_fitness = self.Evaluate_X(X=Moth_pos)
    
            if Iteration == 0:
                # Sort the first population of moths
                fitness_sorted = np.sort(Moth_fitness)
                I = np.argsort(Moth_fitness)
                sorted_population = Moth_pos[I]
                # Update the flames
                best_flames = sorted_population
                best_flame_fitness = fitness_sorted
            else:
                # Sort the moths
                double_population = np.concatenate((previous_population, best_flames), axis=0)
                double_fitness = np.concatenate((previous_fitness, best_flame_fitness), axis=0)
                double_fitness_sorted = np.sort(double_fitness)
                I2 = np.argsort(double_fitness)
                double_sorted_population = double_population[I2]

                fitness_sorted = double_fitness_sorted[0:self.M]
                sorted_population = double_sorted_population[0:self.M]
                # Update the flames
                best_flames = sorted_population
                best_flame_fitness = fitness_sorted

            previous_population = Moth_pos
            previous_fitness = Moth_fitness

            # a linearly dicreases from -1 to -2 to calculate t in Eq. (3.12)
            a = -1 + Iteration * ((-1) / self.budget)
    
            # Loop counter
            for i in range(0, self.M):
                b = 1
                t = (a - 1) * np.random.rand() + 1
                for j in range(0, self.n):
                    distance_to_flame = abs(sorted_population[i, j] - Moth_pos[i, j])
                    if i <= Flame_no:  # Update the position of the moth with respect to its corresponsing flame
                        # D in Eq. (3.13)
                        # Eq. (3.12)
                        Moth_pos[i, j] = distance_to_flame * math.exp(b * t) * math.cos(t * 2 * math.pi)+ sorted_population[i, j]
                    else:
                        # Upaate the position of the moth with respct to one flame
                        #  Eq. (3.13)
                        #  Eq. (3.12)
                        Moth_pos[i, j] = distance_to_flame * math.exp(b * t) * math.cos(t * 2 * math.pi) + sorted_population[Flame_no, j]
                # check boundary
                Moth_pos[i] = np.clip(Moth_pos[i], self.lb_x, self.ub_x)


            Iteration = Iteration + 1
    

            
            
            
            
            
            
            
            
            
            
        

    
   
        
            
 