from .Init_X import Init_X
from .Init_Delta_X import Init_Delta_X
from .Init_Delta_Y import Init_Delta_Y
from .Opt_Delta_X import Opt_Delta_X
from .Opt_Delta_Y import Opt_Delta_Y
from .Opt_X import Opt_X
from .Selection import Selection
from .InitOpt_Delta_z import InitOpt_Delta_z
import numpy as np


class NatureOpt:
    def __init__(self, func, budget_factor = 1e4):
        # inherits objective problem, problem dimension, maximum iteration, problem boundary
        self.fitness_function = func
        self.n = func.meta_data.n_variables
        self.budget = budget_factor * self.n
        self.lb_x = self.fitness_function.constraint.lb[0]
        self.ub_x = self.fitness_function.constraint.ub[1]
        # inherits operations
        # compulsory components
        self.Init_X = Init_X
        self.Opt_X = Opt_X
        self.Selection = Selection
        # elective components
        self.Init_Delta_X = Init_Delta_X
        self.Init_Delta_Y = Init_Delta_Y
        self.InitOpt_Delta_z = InitOpt_Delta_z
        self.Opt_Delta_X = Opt_Delta_X
        self.Opt_Delta_Y = Opt_Delta_Y


    def Evaluate_X(self, X):
        fitness = [self.fitness_function(x) for x in X]
        return np.array(fitness)

    # def Personal_best(self, new_X, new_X_Fit, old_X_p = None, old_X_p_Fit = None):
    #     if old_X_p is None:
    #         new_X_p = new_X
    #         new_X_p_Fit = new_X_Fit
    #         return new_X_p, new_X_p_Fit
    #     else:
    #         new_X_p = old_X_p
    #         new_X_p_Fit = old_X_p_Fit
    #         for i, x in enumerate(new_X):
    #             if new_X_Fit[i] < old_X_p_Fit[i]:
    #                 new_X_p[i] = x
    #                 new_X_p_Fit[i] = new_X_Fit[i]
    #         return new_X_p, new_X_p_Fit
    #
    # def Global_best(self, new_X, new_X_Fit, old_x_g = None, old_x_g_fit = None):
    #     if old_x_g is None:
    #         best_index = np.argmin(new_X_Fit)
    #         x_g_fit = new_X_Fit[best_index]
    #         x_g = new_X[best_index]
    #         return x_g, x_g_fit
    #     else:
    #         xs = np.append([old_x_g],new_X, axis=0)
    #         fits = np.append([old_x_g_fit], new_X_Fit, axis=0)
    #         best_index = np.argmin(fits)
    #         x_g_fit = fits[best_index]
    #         x_g = xs[best_index]
    #         return x_g, x_g_fit

    @property
    def stop(self):
        return self.fitness_function.state.evaluations >= self.budget or self.fitness_function.state.current_best_internal.y < 1e-8
    