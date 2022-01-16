import numpy as np

class Init_Delta_X:
    @staticmethod
    def your():
        pass

    @staticmethod
    def Personal_best(new_X, new_X_Fit):
        new_X_p = new_X
        new_X_p_Fit = new_X_Fit
        return new_X_p, new_X_p_Fit

    @staticmethod
    def Global_best(new_X, new_X_Fit):
        best_index = np.argmin(new_X_Fit)
        x_g_fit = new_X_Fit[best_index]
        x_g = new_X[best_index]
        return x_g, x_g_fit

    @staticmethod
    # this is a special one
    def Sort_X(new_X, new_X_Fit):
        sort_X_ind = np.argsort(new_X_Fit)  # from minimum to maximum
        sort_X = new_X[sort_X_ind]
        sort_X_Fit = new_X_Fit[sort_X_ind]
        return sort_X, sort_X_Fit

