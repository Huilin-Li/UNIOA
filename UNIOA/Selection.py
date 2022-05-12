import numpy as np

class Selection:
    @staticmethod
    def same_type(temp_X, temp_X_Fit): # pso, mfo, goa, csa
        new_X = temp_X
        new_X_Fit = temp_X_Fit
        return new_X, new_X_Fit

    @staticmethod
    def elitism_type(temp_X, temp_X_Fit, old_X, old_X_Fit, elitism): # mbo
        # keep elitists in old_X
        sorted_old_X_inx = np.argsort(old_X_Fit)
        elitists_inx = sorted_old_X_inx[:elitism]
        elitists_x = old_X[elitists_inx]
        elitists_x_fit = old_X_Fit[elitists_inx]

        # replace keep worst x in temp_X by elitists
        new_X_inx = np.argsort(temp_X_Fit)
        new_X = temp_X[new_X_inx]
        new_X_Fit = temp_X_Fit[new_X_inx]
        for i in range(elitism):
            new_X[-(i + 1)] = elitists_x[i]
            new_X_Fit[-(i + 1)] = elitists_x_fit[i]
        return new_X, new_X_Fit

    @staticmethod
    def ba_type(temp_X, temp_X_Fit, old_X, old_X_Fit, z2):
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        M = len(old_X)
        for i in range(M):
            if (np.random.rand() > z2) and (temp_X_Fit[i] < old_X_Fit[i]):
                new_X[i] = temp_X[i]
                new_X_Fit[i] = temp_X_Fit[i]
        return new_X, new_X_Fit

    @staticmethod
    def improve_type(temp_X, temp_X_Fit, old_X, old_X_Fit): # boa
        M = len(temp_X)
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        for i in range(M):
            if temp_X_Fit[i] < old_X_Fit[i]:
                new_X[i] = temp_X[i]
                new_X_Fit[i] = temp_X_Fit[i]
        return new_X, new_X_Fit
