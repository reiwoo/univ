import numpy as np
import scipy.linalg as la

n_v = 7
A_v = np.zeros((n_v, n_v), dtype=float)
for i in range(n_v):
    A_v[i, i] = 2.0
    if i > 0:
        A_v[i, i-1] = -1.0
    if i < n_v - 1:
        A_v[i, i+1] = -1.0
b_v = np.array([3, -4, 4, -4, 4, -4, -3], dtype=float)
A_g = np.array([
    [10, -1,  0,  0,  0,  0],
    [1, -10,  3,  0,  0,  0],
    [0,   1, -10, -2, 0,  0],
    [0,   0,  2, -10, -1, 0],
    [0,   0,  0,   1, -10, 1],
    [0,   0,  0,   0,   2, -10]
], dtype=float)
b_g = np.array([10, 4, -10, 1, -10, 2], dtype=float)



def progon(a, b, c, d):
    n = len(b)
    alpha = np.zeros(n)
    beta = np.zeros(n)

    alpha[0] = -c[0] / b[0]
    beta[0] = d[0] / b[0]
    for i in range(1, n):
        den = b[i] + a[i-1] * alpha[i-1]
        if abs(den) < 1e-14:
            raise ZeroDivisionError("нулевой знаменатель в прогонке")
        if i < n - 1:
            alpha[i] = -c[i] / den
        beta[i] = (d[i] - a[i-1] * beta[i-1]) / den
        
    x = np.zeros(n)
    x[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i+1] + beta[i]
    return x

for name, A, b in [("v", A_v, b_v), ("g", A_g, b_g)]:
    x = progon(np.diag(A, -1), np.diag(A), np.diag(A, 1), b)
    x_ref = la.solve(A, b)
    print(f"{name}: x = {x}")
    print(f"   ||x - x_ref|| = {np.linalg.norm(x - x_ref):.2e}, ||Ax - b|| = {np.linalg.norm(A @ x - b):.2e}")