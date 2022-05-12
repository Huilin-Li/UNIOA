import numpy as np

class InitOpt_Delta_z:
    @staticmethod
    def ba1(t, z1_0, w1):
        new_z1 = z1_0 * (1 - np.exp(-w1 * t))
        return new_z1

    @staticmethod
    def ba2(old_z2, w2):
        new_z2 = w2 * old_z2
        return new_z2

    @staticmethod
    def goa(t, z_interval, T):
        z = z_interval[1] - t * ((z_interval[1] - z_interval[0]) / T)
        return z

# csa no z

    @staticmethod
    def boa(t, old_z, budget):
        # sensory_modality_update in original paper
        if t == 0:
            new_z = old_z
            return new_z
        else:
            new_z = old_z + 0.025 / (old_z*budget)
            return new_z

    @staticmethod
    def mbo(t, w4):
        t = t + 1
        return w4 / (t * t)

    @staticmethod
    def mfo1(t,budget):
        return (-2 - t / budget) * np.random.rand() + 1

    @staticmethod
    def mfo2(t, M, budget):
        return round(M - t * ((M - 1) /budget))
