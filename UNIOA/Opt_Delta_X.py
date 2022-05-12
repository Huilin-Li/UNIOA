import numpy as np

class Opt_Delta_X:
    @staticmethod
    def Personal_best(new_X, new_X_Fit, old_X_p, old_X_p_Fit):
        new_X_p = old_X_p.copy()
        new_X_p_Fit = old_X_p_Fit.copy()
        for i, x in enumerate(new_X):
            if new_X_Fit[i] < old_X_p_Fit[i]:
                new_X_p[i] = x
                new_X_p_Fit[i] = new_X_Fit[i]
        return new_X_p, new_X_p_Fit

    @staticmethod
    def Global_best(new_X, new_X_Fit, old_x_g, old_x_g_fit):
        xs = np.append([old_x_g],new_X, axis=0)
        fits = np.append([old_x_g_fit], new_X_Fit, axis=0)
        best_index = np.argmin(fits)
        x_g_fit = fits[best_index]
        x_g = xs[best_index]
        return x_g, x_g_fit

    @staticmethod
    def Sort_X(new_X, new_X_Fit, old_X, old_X_Fit):
        M = old_X.shape[0]
        double_X = np.concatenate((old_X, new_X), axis=0)
        double_X_Fit = np.concatenate((old_X_Fit, new_X_Fit))
        sorted_double_X_ind = np.argsort(double_X_Fit)
        sort_X = double_X[sorted_double_X_ind][:M]
        sort_X_Fit = double_X_Fit[sorted_double_X_ind][:M]
        return sort_X, sort_X_Fit