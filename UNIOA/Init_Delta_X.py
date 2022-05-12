import numpy as np

class Init_Delta_X:
    @staticmethod
    def Personal_best(new_X, new_X_Fit):
        new_X_p = new_X.copy()
        new_X_p_Fit = new_X_Fit.copy()
        return new_X_p, new_X_p_Fit

    @staticmethod
    def Global_best(new_X, new_X_Fit):
        best_index = np.argmin(new_X_Fit)
        x_g_fit = new_X_Fit[best_index]
        x_g = new_X[best_index]
        return x_g, x_g_fit

    @staticmethod
    def Sort_X(new_X, new_X_Fit):
        sort_X_ind = np.argsort(new_X_Fit) # from minimum value to maximum value
        sort_X = new_X[sort_X_ind]
        sort_X_Fit = new_X_Fit[sort_X_ind]
        return sort_X, sort_X_Fit

