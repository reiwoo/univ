import time
import numpy as np
import scipy.linalg as la

np.set_printoptions(precision=5, suppress=True, linewidth=120)

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


def make_LU_matrix(n, rng, eps=1e-2):
    L = np.tril(rng.uniform(-1, 1, (n, n)), -1) + np.diag(rng.uniform(eps, 2*eps, n))
    U = np.triu(rng.uniform(-1, 1, (n, n)), 1)  + np.diag(rng.uniform(eps, 2*eps, n))
    return L @ U

def timeit(f, reps=200):
    f()
    t = time.perf_counter()
    for _ in range(reps):
        res = f()
    return res, (time.perf_counter() - t) / reps

def part2(ns=range(10, 21), seed=0, eps=1e-2):
    rng = np.random.default_rng(seed)
    print(f"\n{'n':>3s} {'cond(A)':>10s} | {'LU: невязка':>11s} {'отн.ош.':>9s} {'t,сек':>10s} | "
          f"{'QR: невязка':>11s} {'отн.ош.':>9s} {'t,сек':>10s} | {'Rf: отн.ош.':>11s} {'t,сек':>8s}")
    for n in ns:
        A = make_LU_matrix(n, rng, eps)
        x = rng.standard_normal(n)
        b = A @ x
        def solve_lu():
            return la.lu_solve(la.lu_factor(A), b)
        def solve_qr():
            Q, R = la.qr(A)
            return la.solve_triangular(R, Q.T @ b)
        def solve_reflect():
            Q, R = qr_reflect(A)
            return la.solve_triangular(R, Q.T @ b)
        
        row = [f"{n:3d} {np.linalg.cond(A):10.2e} |"]
        for k, f in enumerate([solve_lu, solve_qr, solve_reflect]):
            xs, t = timeit(f)
            r = np.linalg.norm(b - A @ xs)
            rel = np.linalg.norm(xs - x) / np.linalg.norm(x)
            if k < 2: 
                row.append(f"{r:11.2e} {rel:9.2e} {t:10.2e} |")
            else:     
                row.append(f"{rel:11.2e} {t:10.2e}")
        print(" ".join(row))

if __name__ == "__main__":
    n = 10
    for eps in (0.3, 0.1, 1e-2):
        print(f"\n[[[[[[[[[[[[[[[  LU with ~ [{eps}-{2*eps}  ]]]]]]]]]]]]]]]]]]]]]")
        part2(eps=eps)