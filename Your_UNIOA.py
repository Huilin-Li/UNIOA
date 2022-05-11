from UNIOA import *


class UNIOA_create(NatureOpt):
    def __init__(self, func, hyperparams_set, **kwargs):
        super().__init__(func)
        self.M = hyperparams_set.get('M')
        self.Selection = kwargs.get('Selection')

    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)


        # Optimizing
        while not self.stop:

            temp_X = self.Opt_X.your(old_x=X, y=new_Y,)
            temp_X_Fit = self.Evaluate_X(X=X)
            new_X, new_X_Fit = self.Selection(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit)

            t = t + 1
            X_g, X_g_Fit = self.Opt_Delta_X.your(new_X=new_X, new_X_Fit=new_X_Fit)
            X = new_X
            X_Fit = new_X_Fit





