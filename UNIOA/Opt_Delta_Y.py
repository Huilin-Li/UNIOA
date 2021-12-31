import numpy as np

class Opt_Delta_Y:
    @staticmethod
    def your():
        pass
    @staticmethod
    def pso(old_X, old_Y, old_X_p, old_x_g, w1, w2, w3):
        new_Y = old_Y.copy()
        for i, old_y in enumerate(old_Y):
            new_Y[i] = w1 * old_y \
                       + np.random.uniform(0, w2) * (old_X_p[i] - old_X[i]) \
                       + np.random.uniform(0, w3) * (old_x_g - old_X[i])  # update equation.
            return new_Y
 
    @staticmethod
    def ba(old_Y, old_X, old_x_g, w4_interval):
        new_Y = old_Y.copy()
        for i in range(len(new_Y)):
            new_Y[i] = old_Y[i] + np.random.uniform(w4_interval[0], w4_interval[1]) * (old_X[i] - old_x_g)
        return new_Y

    @staticmethod
    def mfo(t, old_Y, fitness_function, old_X, old_X_Fit):
        old_Y_Fit = np.array([fitness_function(y) for y in old_Y])
        if t == 0:
            I = np.argsort(old_Y_Fit)
            new_Y = old_Y[I]
        else:
            Y_Fit_d = np.concatenate((old_Y_Fit, old_X_Fit))
            Y_d = np.concatenate((old_Y, old_X), axis=0)
            I_s_d = np.argsort(Y_Fit_d)
            new_Y_d = Y_d[I_s_d]
            new_Y = new_Y_d[:len(old_X)]

        # old_Y_Fit = np.array([fitness_function(y) for y in old_Y])
        # Y_Fit_d = np.concatenate((old_Y_Fit, old_X_Fit))
        # Y_d = np.concatenate((old_Y, old_X), axis=0)
        # I_s_d = np.argsort(Y_Fit_d)
        # new_Y_d = Y_d[I_s_d]
        # new_Y = new_Y_d[:len(old_X)]
        return new_Y

    @staticmethod
    def csa(old_Y, fitness_function, old_X, old_X_Fit):
       new_Y = old_Y.copy()
       M = len(old_X)
       for i in range(M):
           old_y_fit = fitness_function(old_Y[i])
           if old_X_Fit[i] < old_y_fit:
               new_Y[i] = old_X[i]
       return new_Y






