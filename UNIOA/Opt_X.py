from sklearn.metrics import pairwise_distances
from UNIOA_Framework.LevyFlight import Levy
import numpy as np
from numba import jit, prange

class Opt_X:
    # <editor-fold desc="2 defs for ba: ba, ba_but_asyncE">
    @staticmethod
    def ba(old_X, new_Y, old_x_g, old_z1, old_z2, w3, lb_x, ub_x):
        new_X = old_X.copy()
        n = old_X.shape[1]
        for i, y in enumerate(new_Y):
            x = old_X[i] + y
            if np.random.rand() < old_z1:
                x = old_x_g + w3 * np.random.randn(n) * old_z2
            new_X[i] = np.clip(x, lb_x, ub_x)
        return new_X

    @staticmethod
    def ba_but_asyncE(func, old_X, old_X_Fit, new_Y, old_x_g, old_z1, old_z2, w3, lb_x, ub_x):
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        n = old_X.shape[1]
        for i, y in enumerate(new_Y):
            x = old_X[i] + y
            if np.random.rand() < old_z1:
                x = old_x_g + w3 * np.random.randn(n) * old_z2
            new_X[i] = np.clip(x, lb_x, ub_x)
            new_X_Fit[i] = func(new_X[i])
        return new_X, new_X_Fit
    # </editor-fold>

    # <editor-fold desc="2 defs for goa: goa, goa_but_asyncE">
    @staticmethod
    @jit(parallel=True)
    def goa(old_X, old_x_g, z, lb_x, ub_x, w1, w2):
        M, n = old_X.shape[0], old_X.shape[1]
        new_X = old_X.copy()
        Dist = pairwise_distances(old_X, metric='euclidean')
        for i in prange(M):
            Delta_X = np.zeros(n)
            for j in range(M):
                if i != j:
                    # js are neighbors
                    D = Dist[i, j]
                    norm_D = 2 + np.remainder(D, 2)
                    delta_x = z * ((ub_x - lb_x) / 2) * \
                              (w1 * np.exp(-norm_D / w2) - np.exp(-norm_D)) * \
                              ((old_X[i] - old_X[j]) / (D + 2.2204e-16))
                    Delta_X = Delta_X + delta_x
            new_X[i] = np.clip(z * Delta_X + old_x_g, lb_x, ub_x)
        return new_X

    @staticmethod
    def goa_but_asyncE(func, old_X, old_X_Fit, old_x_g, z, lb_x, ub_x, w1, w2):
        M, n = old_X.shape[0], old_X.shape[1]
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        Dist = pairwise_distances(old_X, metric='euclidean')
        for i in prange(M):
            Delta_X = np.zeros(n)
            for j in range(M):
                if i != j:
                    # js are neighbors
                    D = Dist[i, j]
                    norm_D = 2 + np.remainder(D, 2)
                    delta_x = z * ((ub_x - lb_x) / 2) * \
                              (w1 * np.exp(-norm_D / w2) - np.exp(-norm_D)) * \
                              ((old_X[i] - old_X[j]) / (D + 2.2204e-16))
                    Delta_X = Delta_X + delta_x
            new_X[i] = np.clip(z * Delta_X + old_x_g, lb_x, ub_x)
            new_X_Fit[i] = func(new_X[i])
        return new_X, new_X_Fit
    # </editor-fold>

    # <editor-fold desc="2 defs for csa: csa, ba_but_asyncE">
    @staticmethod
    def csa(old_X, X_p, w1, w2, lb_x, ub_x):
        new_X = old_X.copy()
        M, n = old_X.shape[0], old_X.shape[1]
        for i in range(M):
            if np.random.rand() > w1:
                new = old_X[i] + np.random.rand() * w2 * (X_p[np.random.randint(M)] - old_X[i])
                if np.all(new >= lb_x) & np.all(new <= ub_x):
                    new_X[i] = new
            else:
                new_X[i] = np.random.uniform(lb_x, ub_x, n)
        return new_X

    @staticmethod
    def csa_but_asyncE(func, old_X, old_X_Fit, X_p, w1, w2, lb_x, ub_x):
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        M, n = old_X.shape[0], old_X.shape[1]
        for i in range(M):
            if np.random.rand() > w1:
                new = old_X[i] + np.random.rand() * w2 * (X_p[np.random.randint(M)] - old_X[i])
                if np.all(new >= lb_x) & np.all(new <= ub_x):
                    new_X[i] = new
            else:
                new_X[i] = np.random.uniform(lb_x, ub_x, n)
            new_X_Fit[i] = func(new_X[i])
        return new_X, new_X_Fit
    # </editor-fold>

    # <editor-fold desc="2 defs for mfo: mfo, mfo_but_asyncE">
    @staticmethod
    def mfo(old_X, sort_X, z1, z2, w, lb_x, ub_x):
        new_X = old_X.copy()
        for i, sort_x in enumerate(sort_X):
            temp = abs(sort_x - old_X[i]) * np.exp(w * z1) * np.cos(z1 * 2 * np.pi)
            if i <= z2:
                x = temp + sort_x
            else:
                x = temp + sort_X[z2]
            new_X[i] = np.clip(x, lb_x, ub_x)
        return new_X

    @staticmethod
    def mfo_but_asyncE(func, old_X, old_X_Fit, sort_X, z1, z2, w, lb_x, ub_x):
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        for i, sort_x in enumerate(sort_X):
            temp = abs(sort_x - old_X[i]) * np.exp(w * z1) * np.cos(z1 * 2 * np.pi)
            if i <= z2:
                x = temp + sort_x
            else:
                x = temp + sort_X[z2]
            new_X[i] = np.clip(x, lb_x, ub_x)
            new_X_Fit[i] = func(new_X[i])
        return new_X, new_X_Fit
    # </editor-fold>

    # <editor-fold desc="2 defs for mbo: mbo, mbo_but_asyncE">
    @staticmethod
    @jit(parallel=True)
    def mbo(old_X, old_X_Fit, x_g, z, w1, w2, w3, budget):
        M, n = old_X.shape[0], old_X.shape[1]
        I_s = np.argsort(old_X_Fit)
        sorted_X = old_X[I_s]
        n_strongs = int(np.ceil(w1 * M))
        n_weaks = M - n_strongs
        strong_pop = sorted_X[0:n_strongs]
        weak_pop = sorted_X[n_strongs:]
        # strong
        new_strongs = strong_pop.copy()
        tfs_strong = np.random.rand(n_strongs, n) * w2 <= w1
        for i in prange(n_strongs):
            for d in prange(n):
                if tfs_strong[i, d]:
                    new_strongs[i, d] = strong_pop[np.random.randint(n_strongs), d]
                else:
                    new_strongs[i, d] = weak_pop[np.random.randint(n_weaks), d]

        # weak
        new_weaks = weak_pop.copy()
        tfs_weak = np.random.rand(n_weaks, n) <= w1
        for i in prange(n_weaks):
            for d in prange(n):
                if tfs_weak[i, d]:
                    new_weaks[i, d] = x_g[d]
                else:
                    y = Levy(n=n, T=budget)
                    new_weaks[i, d] = weak_pop[np.random.randint(n_weaks), d]
                    if np.random.rand() > w3:
                        new_weaks[i, d] = new_weaks[i, d] + z * y[d]

        temp_X = np.concatenate((new_strongs, new_weaks))
        return temp_X

    @staticmethod
    def mbo_but_asyncE(func, old_X, old_X_Fit, x_g, z, w1, w2, w3, budget):
        M, n = old_X.shape[0], old_X.shape[1]
        I_s = np.argsort(old_X_Fit)
        sorted_X = old_X[I_s]
        n_strongs = int(np.ceil(w1 * M))
        n_weaks = M - n_strongs
        strong_pop = sorted_X[0:n_strongs]
        weak_pop = sorted_X[n_strongs:]
        # strong
        new_strongs = strong_pop.copy()
        new_strongs_f = old_X_Fit.copy()[0:n_strongs]
        tfs_strong = np.random.rand(n_strongs, n) * w2 <= w1
        for i in prange(n_strongs):
            for d in prange(n):
                if tfs_strong[i, d]:
                    new_strongs[i, d] = strong_pop[np.random.randint(n_strongs), d]
                else:
                    new_strongs[i, d] = weak_pop[np.random.randint(n_weaks), d]
            new_strongs_f[i] = func(new_strongs[i])

        # weak
        new_weaks = weak_pop.copy()
        new_weaks_f = old_X_Fit.copy()[n_strongs:]
        tfs_weak = np.random.rand(n_weaks, n) <= w1
        for i in prange(n_weaks):
            for d in prange(n):
                if tfs_weak[i, d]:
                    new_weaks[i, d] = x_g[d]
                else:
                    y = Levy(n=n, T=budget)
                    new_weaks[i, d] = weak_pop[np.random.randint(n_weaks), d]
                    if np.random.rand() > w3:
                        new_weaks[i, d] = new_weaks[i, d] + z * y[d]
            new_weaks_f[i] = func(new_weaks[i])

        new_X = np.concatenate((new_strongs, new_weaks))
        new_X_Fit = np.concatenate((new_strongs_f, new_weaks_f))
        return new_X, new_X_Fit
    # </editor-fold>

    # <editor-fold desc="2 defs for boa: boa, boa_but_asyncE">
    @staticmethod
    def boa(old_X, old_X_Fit, x_g, z, w1, w2, lb_x, ub_x):
        M = len(old_X)
        new_X = old_X.copy()
        for i in range(M):
            if np.random.rand() > w2:
                temp = np.random.rand() ** 2 * x_g - old_X[i]
                x = old_X[i] + temp * z * old_X_Fit[i] ** w1
            else:
                jk = np.random.choice(M, 2, replace=False)  # two indices of two neighbors
                temp = np.random.rand() ** 2 * old_X[jk[0]] - old_X[jk[1]]
                x = old_X[i] + temp * z * old_X_Fit[i] ** w1
            new_X[i] = np.clip(x, lb_x, ub_x)
        return new_X

    @staticmethod
    def boa_but_asyncE(func, old_X, old_X_Fit, x_g, z, w1, w2, lb_x, ub_x):
        M = len(old_X)
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        for i in range(M):
            if np.random.rand() > w2:
                temp = np.random.rand() ** 2 * x_g - old_X[i]
                x = old_X[i] + temp * z * old_X_Fit[i] ** w1
            else:
                jk = np.random.choice(M, 2, replace=False)  # two indices of two neighbors
                temp = np.random.rand() ** 2 * old_X[jk[0]] - old_X[jk[1]]
                x = old_X[i] + temp * z * old_X_Fit[i] ** w1
            new_X[i] = np.clip(x, lb_x, ub_x)
            new_X_Fit[i] = func(new_X[i])
        return new_X, new_X_Fit
    # </editor-fold>

    # <editor-fold desc="2 defs for pso: pso, pso_but_asyncE">
    @staticmethod
    def pso(old_X, new_Y, lb_x, ub_x):
        new_X = old_X.copy()
        for i, y in enumerate(new_Y):
            x = old_X[i] + y  # update equation.
            new_X[i] = np.clip(x, lb_x, ub_x)
        return new_X

    @staticmethod
    def pso_but_asyncE(func, old_X, old_X_Fit, new_Y, lb_x, ub_x):
        new_X = old_X.copy()
        new_X_Fit = old_X_Fit.copy()
        for i, y in enumerate(new_Y):
            x = old_X[i] + y  # update equation.
            new_X[i] = np.clip(x, lb_x, ub_x)
            new_X_Fit[i] = func(new_X[i])
        return new_X, new_X_Fit
    # </editor-fold>







    


    # @staticmethod
    # def mfo(old_X, sort_X, z1, z2, w, lb_x, ub_x):
    #     new_X = old_X.copy()
    #     for i, sort_x in enumerate(sort_X):
    #         temp = abs(sort_x - old_X[i]) * np.exp(w * z1) * np.cos(z1 * 2 * np.pi)
    #         if i <= z2:
    #             x = temp + sort_x
    #         else:
    #             x = temp + sort_X[z2]
    #         new_X[i] = np.clip(x, lb_x, ub_x)
    #     return new_X


    # @staticmethod
    # def ba(old_X, new_Y, old_x_g, old_z1, old_z2, w3, lb_x, ub_x):
    #     new_X = old_X.copy()
    #     n = old_X.shape[1]
    #     for i, y in enumerate(new_Y):
    #         x = old_X[i] + y
    #         if np.random.rand() < old_z1:
    #             x = old_x_g + w3 * np.random.randn(n) * old_z2
    #         new_X[i] = np.clip(x, lb_x, ub_x)
    #     return new_X
    #
    # @staticmethod
    # def ba_but_asyncE(func, old_X, old_X_Fit,  new_Y, old_x_g, old_z1, old_z2, w3, lb_x, ub_x):
    #     new_X = old_X.copy()
    #     new_X_Fit = old_X_Fit.copy()
    #     n = old_X.shape[1]
    #     for i, y in enumerate(new_Y):
    #         x = old_X[i] + y
    #         if np.random.rand() < old_z1:
    #             x = old_x_g + w3 * np.random.randn(n) * old_z2
    #         new_X[i] = np.clip(x, lb_x, ub_x)
    #         new_X_Fit[i] = func(new_X[i])
    #     return new_X, new_X_Fit


    # @staticmethod
    # def csa(old_X, X_p, w1, w2, lb_x, ub_x):
    #     new_X = old_X
    #     N, n = old_X.shape[0], old_X.shape[1]
    #     for i in range(N):
    #         if np.random.rand() > w1:
    #             new = old_X[i] + np.random.rand() * w2 * (X_p[np.random.randint(N)] - old_X[i])
    #             if np.all(new >=lb_x) & np.all(new <= ub_x):
    #                 new_X[i] = new
    #         else:
    #             new_X[i] = np.random.uniform(lb_x, ub_x, n)
    #     return new_X

    # @staticmethod
    # @jit(parallel=True)
    # def goa(old_X, old_x_g, z, lb_x, ub_x, w1, w2):
    #     N, n = old_X.shape[0], old_X.shape[1]
    #     new_X =old_X.copy()
    #     Dist = pairwise_distances(old_X, metric='euclidean')
    #     for i in prange(N):
    #         Delta_X = np.zeros(n)
    #         for j in range(N):
    #             if i != j:
    #                 # js are neighbors
    #                 D = Dist[i, j]
    #                 norm_D = 2 + np.remainder(D, 2)
    #                 delta_x = z * ((ub_x - lb_x) / 2) * \
    #                           (w1 * np.exp(-norm_D/w2)-np.exp(-norm_D)) * \
    #                           ((old_X[i] - old_X[j])/(D+2.2204e-16))
    #                 Delta_X = Delta_X + delta_x
    #         new_X[i] = np.clip(z * Delta_X + old_x_g, lb_x, ub_x)
    #     return new_X

    # @staticmethod
    # @jit(parallel=True)
    # def mbo(old_X, old_X_Fit, x_g, z, w1, w2, w3, budget):
    #     N, n = old_X.shape[0], old_X.shape[1]
    #     I_s = np.argsort(old_X_Fit)
    #     sorted_X = old_X[I_s]
    #     n_strongs = int(np.ceil(w1 * N))
    #     n_weaks = N - n_strongs
    #     strong_pop = sorted_X[0:n_strongs]
    #     weak_pop = sorted_X[n_strongs:]
    #     # strong
    #     new_strongs = strong_pop.copy()
    #     tfs_strong = np.random.rand(n_strongs, n) * w2 <= w1
    #     for i in prange(n_strongs):
    #         for d in prange(n):
    #             if tfs_strong[i, d]:
    #                 new_strongs[i, d] = strong_pop[np.random.randint(n_strongs), d]
    #             else:
    #                 new_strongs[i, d] = weak_pop[np.random.randint(n_weaks), d]
    #
    #     # weak
    #     new_weaks = weak_pop.copy()
    #     tfs_weak = np.random.rand(n_weaks, n) <= w1
    #     for i in prange(n_weaks):
    #         for d in prange(n):
    #             if tfs_weak[i, d]:
    #                 new_weaks[i, d] = x_g[d]
    #             else:
    #                 y = Levy(n=n, T=budget)
    #                 new_weaks[i, d] = weak_pop[np.random.randint(n_weaks), d]
    #                 if np.random.rand() > w3:
    #                     new_weaks[i, d] = new_weaks[i, d] + z * y[d]
    #
    #
    #     temp_X = np.concatenate((new_strongs, new_weaks))
    #     return temp_X


    # @staticmethod
    # def boa(old_X, old_X_Fit, x_g, z, w1, w2,lb_x, ub_x):
    #     N = len(old_X)
    #     new_X = old_X.copy()
    #     for i in range(N):
    #         if np.random.rand()>w2:
    #             temp = np.random.rand() ** 2 * x_g - old_X[i]
    #             x = old_X[i] + temp * z * old_X_Fit[i] ** w1
    #         else:
    #             jk = np.random.choice(N, 2, replace=False) # two indices of two neighbors
    #             temp = np.random.rand()**2*old_X[jk[0]]-old_X[jk[1]]
    #             x = old_X[i] + temp * z * old_X_Fit[i] ** w1
    #         new_X[i] = np.clip(x, lb_x, ub_x)
    #     return new_X


