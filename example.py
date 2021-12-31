from UNIOA import *

# main optimization on x
def your_Opt_X(old_x, y, x_ip, z, w):
    new_x = ( old_x * z - y )*w + x_ip
    return new_x
Opt_X.your = your_Opt_X

# influencing factors
## influencing factor y
Init_Delta_Y.your = Init_Delta_Y.x_type
def your_Opt_Delta_Y(old_y, w):
    new_y = old_y * w
    return new_y
Opt_Delta_Y.your = your_Opt_Delta_Y

## influencing factor x-related
Init_Delta_X.your = Init_Delta_X.Personal_best
Opt_Delta_X.your = Opt_Delta_X.Personal_best

## influencing factor z
def your_InitOpt_Delta_z(t, old_z, w):
    if t == 0:
        new_z = old_z
    else:
        new_z = old_z * w
    return new_z
InitOpt_Delta_z.your = your_InitOpt_Delta_z

# main optimization on x
def your_Opt_X(old_x, y, x_ip, z, w):
    new_x = ( old_x * z - y )*w + x_ip
    return new_x
Opt_X.your = your_Opt_X

# Selection method
Selection.your = Selection.improve_type
# initialize/setup static numerical influencing factors
M = 10
z_0 = 1 # assizt z
w1 = 0.8 # assist z
w2 = 0.4 # assist to update y
w3 = 0.98 # assist to update x

class Your_Opt(NatureOpt):
    def __init__(self, func, hyperparams_set, budget_factor=1e4):
        super().__init__(func, budget_factor)
        self.M = hyperparams_set.get('M', 10)
        self.z_0 = hyperparams_set.get('z_0', 1)
        self.w1 = hyperparams_set.get('w1', 0.8)
        self.w2 = hyperparams_set.get('w2', 0.4)
        self.w3 = hyperparams_set.get('w3', 0.98)


    def __call__(self):
        t = 0
        X = self.Init_X.Init_X(M=self.M, n=self.n, lb_x=self.lb_x, ub_x=self.ub_x)
        X_Fit = self.Evaluate_X(X=X)
        Y = self.Init_Delta_Y.x_type(X=X)
        X_ip, X_ip_Fit = self.Init_Delta_X.Personal_best(new_X=X, new_X_Fit=X_Fit)
        z = self.InitOpt_Delta_z.your(t=t, old_z=self.z_0,w=self.w1)

        # Optimizing
        while not self.stop:
            new_Y = self.Opt_Delta_Y.your(old_y=Y, w=self.w2)
            temp_X = self.Opt_X.your(old_x=X, y=new_Y, x_ip=X_ip, z=z, w=self.w3)
            temp_X_Fit = self.Evaluate_X(X=X)
            new_X, new_X_Fit = self.Selection.your(temp_X=temp_X, temp_X_Fit=temp_X_Fit, old_X=X, old_X_Fit=X_Fit)

            t = t + 1
            z = self.InitOpt_Delta_z.your(t=t, old_z=z,w=self.w1)
            X_ip, X_ip_Fit = self.Opt_Delta_X.your(new_X=new_X, new_X_Fit=new_X_Fit, old_X_p=X_ip, old_X_p_Fit=X_ip_Fit)
            X = new_X
            X_Fit = new_X_Fit


if __name__ == '__main__':
    Algs = ['BA_Opt', 'Your_Opt']
    comparison.comparing(Algs)