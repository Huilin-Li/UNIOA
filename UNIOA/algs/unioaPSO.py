from UNIOA_Framework.NatureOpt import NatureOpt


# This class implements PSO-Optimizer in the UNIOA framework.
# E is sync
# G is sync


class PSO_UNIOA(NatureOpt):
    def __init__(self, func ,hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('popsize', 25)
        self.y_interval = hyperparams_set.get('y-interval', [-1, 1])
        self.w1 = hyperparams_set.get('w1', 0.73)
        self.w2 = hyperparams_set.get('w2', 1.49)
        self.w3 = hyperparams_set.get('w3', 1.49)


    # algorithm process
    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
        Y = self.Init_Delta_Y.interval_type(M=self.M, n=self.n, interval=self.y_interval)
        X_p, X_p_Fit = self.Init_Delta_X.Personal_best(new_X=X, new_X_Fit=X_Fit)
        x_g, x_g_fit = self.Init_Delta_X.Global_best(new_X=X, new_X_Fit=X_Fit)
        while not self.stop:
            # Aoptimize y(t+1)
            new_Y = self.Opt_Delta_Y.pso(old_X=X, old_Y=Y, old_X_p=X_p, old_x_g=x_g, w1=self.w1, w2=self.w2, w3=self.w3)
            # Ooptimize x(t+1)
            temp_X = self.Opt_X.pso(old_X=X, new_Y=new_Y, lb_x=self.lb_x, ub_x=self.ub_x)
            # Evaluate
            temp_X_Fit = self.Evaluate_X(X=temp_X)
            # Selection
            new_X, new_X_Fit = self.Selection.same_type(temp_X=temp_X, temp_X_Fit=temp_X_Fit)
            #----------------------------
            t = t + 1
            new_X_p, new_X_p_Fit = self.Opt_Delta_X.Personal_best(new_X=new_X, new_X_Fit=new_X_Fit, old_X_p=X_p, old_X_p_Fit=X_p_Fit)
            new_x_g, new_x_g_fit = self.Opt_Delta_X.Global_best(new_X=new_X, new_X_Fit=new_X_Fit, old_x_g=x_g, old_x_g_fit=x_g_fit)
            ############################
            X = new_X
            Y = new_Y
            X_p, X_p_Fit = new_X_p, new_X_p_Fit
            x_g, x_g_fit = new_x_g, new_x_g_fit