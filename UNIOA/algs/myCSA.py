from UNIOA.NatureOpt import NatureOpt

# -------------------------------------------------------------------------------------------------
# This class implements CSA-Optimizer in the new structure.
# -------------------------------------------------------------------------------------------------

class CSA_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize',50)
        self.w1 = hyperparams_set.get('w1', 0.1)
        self.w2 = hyperparams_set.get('w2', 2)


    
    def __call__(self):
        t = 0  # iteration counter
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)  # Evaluate X
        Y = self.Init_Delta_Y.x_type(X=X)

        # Optimizing
        while not self.stop:
            # AOpt Y(t+1)
            new_Y = self.Opt_Delta_Y.csa(old_Y=Y, fitness_function=self.fitness_function, old_X=X, old_X_Fit=X_Fit)
            # OOpt temp_X(t+1)
            temp_X = self.Opt_X.csa(new_Y=new_Y, old_X=X, w1=self.w1, w2=self.w2, lb_x=self.lb_x, ub_x=self.ub_x)
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.improve_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit)
            # ----------------------------
            t = t + 1
            ##########################
            X = new_X
            X_Fit = new_X_Fit
            Y = new_Y

