from UNIOA_Framework.NatureOpt import NatureOpt


# This class implements GOA-Optimizer in the UNIOA framework.
# E is sync
# G is sync

class GOA_UNIOA(NatureOpt):
    def __init__(self, func, hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 100)
        self.z_interval = hyperparams_set.get('z-interval', [0.00004, 1])
        self.w1 = hyperparams_set.get('w1', 0.5)#=f
        self.w2 = hyperparams_set.get('w2', 1.5)#=l

    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
        x_g, x_g_fit = self.Init_Delta_X.Global_best(new_X=X, new_X_Fit=X_Fit)
        z = self.InitOpt_Delta_z.goa(t=t, z_interval=self.z_interval, T=self.budget)
        # Optimizing
        while not self.stop:
            # Oopt x(t+1)
            temp_X = self.Opt_X.goa(old_X=X, old_x_g = x_g, z=z, lb_x=self.lb_x, ub_x=self.ub_x, w1=self.w1, w2=self.w2)
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.same_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit)
            ########################
            t =  t + 1
            x_g, x_g_fit = self.Opt_Delta_X.Global_best(new_X=new_X, new_X_Fit=new_X_Fit, old_x_g=x_g, old_x_g_fit=x_g_fit)
            z = self.InitOpt_Delta_z.goa(t=t, z_interval=self.z_interval, T=self.budget)
            X = new_X

