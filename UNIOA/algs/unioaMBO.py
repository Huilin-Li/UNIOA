from UNIOA_Framework.NatureOpt import NatureOpt

# This class implements MBO-Optimizer in the UNIOA framework.
# E is sync
# G is sync

class MBO_UNIOA(NatureOpt):
    def __init__(self, func, hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 50)
        self.w1 = hyperparams_set.get('w1', 5 / 12)
        self.w2 = hyperparams_set.get('w2', 1.2)
        self.w3 = hyperparams_set.get('w3', 5 / 12)
        self.w4 = hyperparams_set.get('w4', 1)
        self.w5 = hyperparams_set.get('w5', 2)

    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)  
        X_Fit = self.Evaluate_X(X=X)
        x_g, x_g_fit = self.Init_Delta_X.Global_best(new_X=X, new_X_Fit=X_Fit)
        z = self.InitOpt_Delta_z.mbo(t=t, w4=self.w4)

        # algorithm process
        while not self.stop:
            # OOptimize temp_X(t+1)
            temp_X = self.Opt_X.mbo(old_X=X, old_X_Fit=X_Fit, x_g=x_g, z=z, w1=self.w1, w2=self.w2, w3=self.w3, budget=self.budget)
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.elitism_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit, elitism=self.w5)
            # ----------------------------
            new_z = self.InitOpt_Delta_z.mbo(t=t+1, w4=self.w4)
            new_x_g, new_x_g_fit = self.Opt_Delta_X.Global_best(new_X=new_X, new_X_Fit=new_X_Fit, old_x_g=x_g, old_x_g_fit=x_g_fit)
            # ----------------------------
            X = new_X.copy()
            X_Fit = new_X_Fit.copy()
            x_g, x_g_fit = new_x_g, new_x_g_fit
            z = new_z
            ########################################
            t = t + 1


