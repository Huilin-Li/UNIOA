from UNIOA_Framework.NatureOpt import NatureOpt


# This class implements BOA-Optimizer in the UNIOA framework.
# E is sync
# G is sync

class BOA_UNIOA(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 50)
        self.w1 = hyperparams_set.get('w1', 0.1)#=power exponent
        self.w2 = hyperparams_set.get('w2', 0.8)#=prob
        self.z_0 = hyperparams_set.get('z_0', 0.01)# = sensory modality


    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
        x_g, x_g_fit = self.Init_Delta_X.Global_best(new_X=X, new_X_Fit=X_Fit)
        z = self.InitOpt_Delta_z.boa(t=t, old_z=self.z_0, budget=self.budget)

        while not self.stop:
            # generate temp_X(t+1)
            temp_X = self.Opt_X.boa(old_X=X, old_X_Fit=X_Fit, x_g=x_g, z=z, w1=self.w1, w2=self.w2, lb_x=self.lb_x, ub_x=self.ub_x)
            # evaluate temp_X(t+1)
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # selection
            X, X_Fit = self.Selection.improve_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit)
            # ----------------------------
            x_g, x_g_fit = self.Opt_Delta_X.Global_best(new_X=X, new_X_Fit=X_Fit, old_x_g=x_g, old_x_g_fit=x_g_fit)
            z = self.InitOpt_Delta_z.boa(t=t+1, old_z=z, budget=self.budget)
            #######################################
            t = t + 1

