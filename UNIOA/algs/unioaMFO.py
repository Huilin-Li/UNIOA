from UNIOA.NatureOpt import NatureOpt

# MothFlame-Optimizer in the UNIOA framework.
# E is sync
# G is sync

class MFO_UNIOA(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 30)
        self.w = hyperparams_set.get('w', 1)

    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
        sort_X, sort_X_Fit = self.Init_Delta_X.Sort_X(new_X=X, new_X_Fit=X_Fit)
        z1 = self.InitOpt_Delta_z.mfo1(t=t, budget=self.budget)
        z2 = self.InitOpt_Delta_z.mfo2(t=t, M=self.M, budget=self.budget)

        # optimize process
        while not self.stop:
            # Optimize temp_X(t+1)
            temp_X = self.Opt_X.mfo(old_X=X, sort_X = sort_X, z1=z1, z2=z2, w=self.w, lb_x=self.lb_x, ub_x=self.ub_x )
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.same_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit)
            # ----------------------------
            new_sort_X, new_sort_X_Fit = self.Opt_Delta_X.Sort_X(new_X=new_X, new_X_Fit=new_X_Fit, old_X=X, old_X_Fit=X_Fit)
            new_z1 = self.InitOpt_Delta_z.mfo1(t=t+1, budget=self.budget)
            new_z2 = self.InitOpt_Delta_z.mfo2(t=t+1, M=self.M, budget=self.budget)
            # ----------------------------
            X = new_X.copy()
            X_Fit= new_X_Fit.copy()
            sort_X = new_sort_X.copy()
            z1 = new_z1
            z2 = new_z2
            ##################################
            t = t + 1
