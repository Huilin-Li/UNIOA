import numpy as np
from .Init_Delta_X import Init_Delta_X
from .Init_Delta_Y import Init_Delta_Y
from .InitOpt_Delta_z import InitOpt_Delta_z
from .Opt_X import Opt_X
from .Opt_Delta_X import Opt_Delta_X
from .Opt_Delta_Y import Opt_Delta_Y
from .Selection import Selection
from .Init_X import Init_X


class NatureOpt:
    def __init__(self, func, budget_factor = 1e4):
        # objective problem, problem dimension, maximum iteration, problem boundary
        self.fitness_function = func
        self.n = func.meta_data.n_variables
        self.budget = budget_factor * self.n
        self.lb_x = self.fitness_function.constraint.lb[0]
        self.ub_x = self.fitness_function.constraint.ub[1]
        # compulsory components
        self.Init_X = Init_X
        self.Opt_X = Opt_X
        self.Selection = Selection
        # selective components
        self.Init_Delta_X = Init_Delta_X
        self.Init_Delta_Y = Init_Delta_Y
        self.InitOpt_Delta_z = InitOpt_Delta_z
        self.Opt_Delta_X = Opt_Delta_X
        self.Opt_Delta_Y = Opt_Delta_Y


    def Evaluate_X(self, X):
        fitness = [self.fitness_function(x) for x in X]
        return np.array(fitness)


    @property
    def stop(self):
        return self.fitness_function.state.evaluations >= self.budget or self.fitness_function.state.current_best_internal.y < 1e-8
    