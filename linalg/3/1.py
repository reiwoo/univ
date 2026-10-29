import time
import numpy as np
import scipy.linalg as la

np.set_printoptions(precision=5, suppress=True, linewidth=120)

def create_matrices(n):
    A = np.zeros((n, n), dtype=float)
    B = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i, j] = 2 * i + 1
            elif i == j + 1:
                A[i, j] = i
            elif i == j - 1:
                A[i, j] = j
    for i in range(n):
        for j in range(n):
            B[i, j] = np.sin((i + 1) * (j + 1) / (2 * n))
    print(A)
    print(B)
    return A, B

def qr_rotate(A):
    R = A.astype(float).copy()
    n, m = R.shape
    Q = np.eye(n)
    for j in range(min(n - 1, m)):
        for i in range(n - 1, j, -1):
            a, b = R[i - 1, j], R[i, j]
            if b == 0.0:
                continue
            r = np.hypot(a, b)
            c, s = a / r, b / r
            G = np.array([[c, s], [-s, c]])
            R[[i - 1, i], :] = G @ R[[i - 1, i], :]
            Q[:, [i - 1, i]] = Q[:, [i - 1, i]] @ G.T
            R[i, j] = 0.0
    return Q, R

def qr_orto(A, modified=True):
    A = A.astype(float)
    n, m = A.shape
    Q = np.zeros((n, m))
    R = np.zeros((m, m))
    for j in range(m):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = Q[:, i].T @ (v if modified else A[:, j])
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j]
    return Q, R

def qr_reflect(A):
    A = A.astype(float).copy()
    n, m = A.shape
    Q = np.eye(n)
    for k in range(min(n - 1, m)):
        x = A[k:, k]
        nx = np.linalg.norm(x)
        if nx == 0.0:
            continue
        v = x.copy()
        v[0] += np.copysign(nx, x[0])
        v /= np.linalg.norm(v)
        for j in range(k, m):
            scalar = v @ A[k:, j]
            A[k:, j] -= 2.0 * v * scalar
            
        for i in range(n):
            scalar_q = Q[i, k:] @ v
            Q[i, k:] -= 2.0 * scalar_q * v
        A[k + 1:, k] = 0.0
    return Q, A


methods = {
    "Метод вращений":          qr_rotate,
    "Метод ортог. (класс)":    lambda M: qr_orto(M, modified=False),
    "Метод ортог. (модиф)":    lambda M: qr_orto(M, modified=True),
    "Метод отражения":         qr_reflect,
}

def part1(n=10):
    A, B = create_matrices(n)
    for name, M in [("A", A), ("B", B)]:
        print(f"\n_____________________Matrix [{name}], n [{n}]______________________")
        print(f"{'     Method':26s} {'||Q^T@Q - I||':>17s} {'||Q@Q^T - I||':>16s} {'||Q^R - A||':>13s}")
        I = np.eye(n)
        for mname, f in methods.items():
            Q, R = f(M)
            print(f"{mname:26s} {np.linalg.norm(Q.T@Q - I):15.2e} " 
                  f"{np.linalg.norm(Q@Q.T - I):15.2e} {np.linalg.norm(Q@R - M):15.2e}")
        print(f"[[[cond_2({name}) = {np.linalg.cond(M):.6e}]]]")

# ---------------------------------------------------------------
# Пункт 2: A = L U с малыми диагоналями, решение LU и QR
# ---------------------------------------------------------------
#def make_LU_matrix(n, rng, eps=1e-2):
#    L = np.tril(rng.uniform(-1, 1, (n, n)), -1) + np.diag(rng.uniform(eps, 2*eps, n))
#    U = np.triu(rng.uniform(-1, 1, (n, n)), 1)  + np.diag(rng.uniform(eps, 2*eps, n))
#    return L @ U

#def timeit(f, reps=200):
#    f()  # прогрев
#    t = time.perf_counter()
#    for _ in range(reps):
#        res = f()
#    return res, (time.perf_counter() - t) / reps

#def part2(ns=range(10, 21), seed=0, eps=1e-2):
#    rng = np.random.default_rng(seed)
#    print(f"\n{'n':>3s} {'cond(A)':>10s} | {'LU: невязка':>11s} {'отн.ош.':>9s} {'t,мкс':>7s} | "
#          f"{'QR: невязка':>11s} {'отн.ош.':>9s} {'t,мкс':>7s} | {'Hh: отн.ош.':>11s} {'t,мкс':>8s}")
#    for n in ns:
#        A = make_LU_matrix(n, rng, eps)
#        x = rng.standard_normal(n)
#        b = A @ x
#        def solve_lu():
#            return la.lu_solve(la.lu_factor(A), b)
#        def solve_qr():
#            Q, R = la.qr(A)
#            return la.solve_triangular(R, Q.T @ b)
#        def solve_hh():
#            Q, R = qr_reflect(A)
#            return la.solve_triangular(R, Q.T @ b)
#        row = [f"{n:3d} {np.linalg.cond(A):10.2e} |"]
#        for k, f in enumerate([solve_lu, solve_qr, solve_hh]):
#            xs, t = timeit(f)
#            r = np.linalg.norm(b - A @ xs)
#            rel = np.linalg.norm(xs - x) / np.linalg.norm(x)
#            if k < 2: row.append(f"{r:11.2e} {rel:9.2e} {t*1e6:7.1f} |")
#            else:     row.append(f"{rel:11.2e} {t*1e6:8.1f}")
#        print(" ".join(row))

if __name__ == "__main__":
    n = 10
    part1(n)
    #for eps in (0.3, 0.1, 1e-2):
    #    print(f"\n##### диагонали L и U ~ [{eps}, {2*eps}] #####")
    #    part2(eps=eps)