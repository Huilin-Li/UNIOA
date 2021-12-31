from UNIOA.NatureOpt import NatureOpt

# -------------------------------------------------------------------------------------------------
# This class implements Bat-Optimizer in the new structure.
# -------------------------------------------------------------------------------------------------
class BA_Opt(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 20)
        self.y_interval = hyperparams_set.get('y-interval', [0, 0])
        self.z1_0 = hyperparams_set.get('z1_0', 1)
        self.z2_0 = hyperparams_set.get('z2_0', 1)
        self.w1 = hyperparams_set.get('w1', 0.1)
        self.w2 = hyperparams_set.get('w2', 0.97)
        self.w3 = hyperparams_set.get('w3', 0.1)
        self.w4_interval = hyperparams_set.get('w4-interval', [0, 2])

    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)  # Evaluate X
        Y = self.Init_Delta_Y.interval_type(M=self.M, n=self.n, interval=self.y_interval)
        x_g, x_g_fit = self.Init_Delta_X.Global_best(new_X=X, new_X_Fit=X_Fit)
        z1 = self.InitOpt_Delta_z.ba1(t=t, z1_0=self.z1_0, w1=self.w1)
        z2 = self.InitOpt_Delta_z.ba2(old_z2=self.z2_0, w2=self.w2)

        # Optimizing
        while not self.stop:
            # Aopt y(t+1)
            new_Y = self.Opt_Delta_Y.ba(old_Y=Y, old_X=X, old_x_g=x_g, w4_interval=self.w4_interval)
            # Oopt temp_x(t+1)
            temp_X = self.Opt_X.ba(old_X=X, new_Y=new_Y, old_x_g=x_g, old_z1=z1, old_z2=z2, w3=self.w3, lb_x=self.lb_x, ub_x=self.ub_x )
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.ba_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit,z2=z2)
            # ----------------------------
            t = t + 1
            new_x_g, new_x_g_fit = self.Opt_Delta_X.Global_best(new_X=new_X, new_X_Fit=new_X_Fit, old_x_g=x_g, old_x_g_fit=x_g_fit)
            new_z1 = self.InitOpt_Delta_z.ba1(t=t, z1_0=self.z1_0, w1=self.w1)
            new_z2 = self.InitOpt_Delta_z.ba2(old_z2=z2, w2=self.w2)
            ####################
            X = new_X
            X_Fit = new_X_Fit
            Y = new_Y
            x_g, x_g_fit = new_x_g, new_x_g_fit
            z1 = new_z1
            z2 = new_z2



 