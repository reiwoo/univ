import numpy as np
import scipy.linalg as la

A_a = np.array([
    [6.1,  6.2, 6.3, 6.4],
    [1.1, -1.5, 2.2, -3.8],
    [5.1, -5.0, 4.9, -4.8],
    [1.8,  1.9, 2., -2.1]
], dtype=float)
b_a = np.array([6.5, 4.2, 4.7, 2.2], dtype=float)

A_b = np.array([
    [ 4, -6,   0,  8,  0,  0],
    [-6,  8, -12,  0, 16,  0],
    [ 0,-12,  16,  0,  0,  0],
    [ 8,  0,   0, 20, -8, 0],
    [ 0, 16,   0, -8, 24, -8],
    [ 0,  0,   10, 0, -8, 28]
], dtype=float)
b_b = np.array([24, 54, 84, 48, 72, 158], dtype=float)

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





systems = {"a": (A_a, b_a), "b": (A_b, b_b), "v": (A_v, b_v), "g": (A_g, b_g)}

def solve_lu(A, b):
    P, L, U = la.lu(A)
    y = la.solve_triangular(L, P.T @ b, lower=True)
    x = la.solve_triangular(U, y, lower=False)
    return P, L, U, x
        
def solve_qr(A, b):
    Q, R = la.qr(A)
    x = la.solve_triangular(R, Q.T @ b, lower=False)
    return Q, R, x

def solve_chol(A, b):
    L = la.cholesky(A, lower=True)
    y = la.solve_triangular(L, b, lower=True)
    x = la.solve_triangular(L.T, y, lower=False)
    return L, x

np.set_printoptions(precision=5, suppress=True, linewidth=120)

for name, (A, b) in systems.items():
    print(f"\n_____________________Variant [{name}]_______________________")
    x_ref = la.solve(A, b)

    # a) LU и QR
    P, L, U, x_lu = solve_lu(A, b)
    Q, R, x_qr = solve_qr(A, b)
    print("L =\n", L, "\nU =\n", U)
    print("Q =\n", Q, "\nR =\n", R)
    print("x (LU):", x_lu, " ||x - x_ref|| =", np.linalg.norm(x_lu - x_ref))
    print("x (QR):", x_qr, " ||x - x_ref|| =", np.linalg.norm(x_qr - x_ref))

    # b) Холецкий
    sym = np.allclose(A, A.T)
    if not sym:
        print("Холецкий: матрица несимметрична — не применим.")
        continue
    try:
        L_chol, x_ch = solve_chol(A, b)
        print("Lc =\n", L_chol)
        print("x (Cholesky):", x_ch, " ||x - x_ref|| =", np.linalg.norm(x_ch - x_ref))
    except la.LinAlgError:
        print("Холецкий: матрица НЕ положительно определена.")
        print("Собственные значения:", np.linalg.eigvalsh(A))