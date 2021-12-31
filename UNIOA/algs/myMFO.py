from UNIOA.NatureOpt import NatureOpt

# -------------------------------------------------------------------------------------------------
# MothFlame-Optimizer in the new structure.
# -------------------------------------------------------------------------------------------------

class MFO_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 30)
        self.w = hyperparams_set.get('w', 1)

    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
        Y = self.Init_Delta_Y.x_type(X=X)
        z1 = self.InitOpt_Delta_z.mfo1(t=t, budget=self.budget)
        z2 = self.InitOpt_Delta_z.mfo2(t=t, M=self.M, budget=self.budget)

        # optimize process
        while not self.stop:
            # AOptimize y(t+1)
            new_Y = self.Opt_Delta_Y.mfo(t=t, old_Y=Y, fitness_function=self.fitness_function, old_X=X, old_X_Fit=X_Fit)
            # OOptimize temp_X(t+1)
            temp_X = self.Opt_X.mfo(old_X=X, new_Y=new_Y, z1=z1, z2=z2, w=self.w, lb_x=self.lb_x, ub_x=self.ub_x)
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.same_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit)

            # ----------------------------
            t = t + 1
            new_z1 = self.InitOpt_Delta_z.mfo1(t=t, budget=self.budget)
            new_z2 = self.InitOpt_Delta_z.mfo2(t=t, M=self.M, budget=self.budget)
            ##################################
            X = new_X
            X_Fit= new_X_Fit
            Y = new_Y
            z1 = new_z1
            z2 = new_z2