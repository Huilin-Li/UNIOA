import numpy as np

class Init_Delta_Y:
    @staticmethod
    def interval_type(M, n, interval): # pso, ba
        lb_y = interval[0]
        ub_y = interval[1]
        Y = np.random.uniform(lb_y, ub_y, (M, n))
        return Y


