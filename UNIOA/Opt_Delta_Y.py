from UNIOA_Framework.LevyFlight import *



class Opt_Delta_Y:
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

