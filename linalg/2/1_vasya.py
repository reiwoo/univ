import numpy as np
from scipy.linalg import lu
from scipy.linalg import qr
from scipy.linalg import cholesky
from scipy.linalg import solve_triangular
from scipy.linalg import eigvalsh


def solve_by_lu(A, b):
    P, L, U = lu(A)

    y = solve_triangular(L, P.T @ b, lower=True, unit_diagonal=True)
    x = solve_triangular(U, y)

    return P, L, U, x

def solve_by_qr(A, b):
    Q, R = qr(A)

    y = Q.T @ b
    x = solve_triangular(R, y)

    return Q, R, x

def solve_by_cholesky(A, b):
    L = cholesky(A, lower=True)

    y = solve_triangular(L, b, lower=True)
    x = solve_triangular(L.T, y)

    return L, x

def is_positive_definite(A):
    if not np.allclose(A, A.T):
        return False

    eigenvalues = eigvalsh(A)

    return np.all(eigenvalues > 0)

def print_matrix(name, matrix):
    print(f"{name} =")
    print(np.array2string(matrix, precision=6, suppress_small=True))
    print()

def print_vector(name, vector):
    print(f"{name} =")
    print(np.array2string(vector, precision=10, suppress_small=True))
    print()

A_a = np.array([
    [6.1,  6.2, -6.3,  6.4],
    [1.1, -1.5,  2.2, -3.8],
    [5.1, -5.0,  4.9, -4.8],
    [1.8,  1.9,  2.0, -2.1]
], dtype=float)

b_a = np.array([6.5, 4.2, 4.7, 2.2], dtype=float)

print("=" * 70)
print("СИСТЕМА a)")
print("=" * 70)

print_matrix("A", A_a)
print_vector("b", b_a)

P_a, L_a, U_a, x_a_lu = solve_by_lu(A_a, b_a)

print("LU-РАЗЛОЖЕНИЕ")
print_matrix("P", P_a)
print_matrix("L", L_a)
print_matrix("U", U_a)

print_vector("x (через LU)", x_a_lu)

Q_a, R_a, x_a_qr = solve_by_qr(A_a, b_a)

print("QR-РАЗЛОЖЕНИЕ")
print_matrix("Q", Q_a)
print_matrix("R", R_a)

print_vector("x (через QR)", x_a_qr)

if is_positive_definite(A_a):
    L_chol_a, x_a_chol = solve_by_cholesky(A_a, b_a)

    print("РАЗЛОЖЕНИЕ ХОЛЕЦКОГО")
    print_matrix("L", L_chol_a)
    print_vector("x (через Холецкого)", x_a_chol)
else:
    print("Разложение Холецкого для системы а) не применяется.")

A_b = np.array([
    [4,  -6,   0,  8,  0,  0],
    [-6,  8, -12,  0, 16,  0],
    [0, -12,  16,  0,  0, 10],
    [8,   0,   0, 20, -8,  0],
    [0,  16,  0, -8, 24, -8],
    [0,   0,  10,  0, -8, 28]
], dtype=float)

b_b = np.array([24, 54, 84, 48, 72, 158], dtype=float)

print("=" * 70)
print("СИСТЕМА б)")
print("=" * 70)

print_matrix("A", A_b)
print_vector("b", b_b)

P_b, L_b, U_b, x_b_lu = solve_by_lu(A_b, b_b)

print("LU-РАЗЛОЖЕНИЕ")
print_matrix("P", P_b)
print_matrix("L", L_b)
print_matrix("U", U_b)

print_vector("x (через LU)", x_b_lu)

Q_b, R_b, x_b_qr = solve_by_qr(A_b, b_b)

print("QR-РАЗЛОЖЕНИЕ")
print_matrix("Q", Q_b)
print_matrix("R", R_b)

print_vector("x (через QR)", x_b_qr)

if is_positive_definite(A_b):
    L_chol_b, x_b_chol = solve_by_cholesky(A_b, b_b)

    print("РАЗЛОЖЕНИЕ ХОЛЕЦКОГО")
    print_matrix("L", L_chol_b)
    print_vector("x (через Холецкого)", x_b_chol)
else:
    print("Разложение Холецкого для системы б) не применяется.")

n = 6

A_v = 2 * np.eye(n)

for i in range(n - 1):
    A_v[i, i + 1] = -1
    A_v[i + 1, i] = -1

b_v = np.zeros(n)

b_v[0] = 3
b_v[-1] = -3

for i in range(1, n - 1):
    if i % 2 == 1:
        b_v[i] = -4
    else:
        b_v[i] = 4

print("=" * 70)
print("СИСТЕМА в)")
print("=" * 70)

print_matrix("A", A_v)
print_vector("b", b_v)

P_v, L_v, U_v, x_v_lu = solve_by_lu(A_v, b_v)

print("LU-РАЗЛОЖЕНИЕ")
print_matrix("P", P_v)
print_matrix("L", L_v)
print_matrix("U", U_v)

print_vector("x (через LU)", x_v_lu)

Q_v, R_v, x_v_qr = solve_by_qr(A_v, b_v)

print("QR-РАЗЛОЖЕНИЕ")
print_matrix("Q", Q_v)
print_matrix("R", R_v)

print_vector("x (через QR)", x_v_qr)

if is_positive_definite(A_v):
    L_chol_v, x_v_chol = solve_by_cholesky(A_v, b_v)

    print("РАЗЛОЖЕНИЕ ХОЛЕЦКОГО")
    print_matrix("L", L_chol_v)
    print_vector("x (через Холецкого)", x_v_chol)
else:
    print("Разложение Холецкого для системы в) не применяется.")

A_g = np.array([
    [10, -1,  0,  0,  0,  0],
    [1, -10,  3,  0,  0,  0],
    [0,   1, -10, -2, 0,  0],
    [0,   0,  2, -10, -1, 0],
    [0,   0,  0,   1, -10, 1],
    [0,   0,  0,   0,   2, -10]
], dtype=float)

b_g = np.array([10, 4, -10, 1, -10, 2], dtype=float)

print("=" * 70)
print("СИСТЕМА г)")
print("=" * 70)

print_matrix("A", A_g)
print_vector("b", b_g)

P_g, L_g, U_g, x_g_lu = solve_by_lu(A_g, b_g)

print("LU-РАЗЛОЖЕНИЕ")
print_matrix("P", P_g)
print_matrix("L", L_g)
print_matrix("U", U_g)

print_vector("x (через LU)", x_g_lu)

Q_g, R_g, x_g_qr = solve_by_qr(A_g, b_g)

print("QR-РАЗЛОЖЕНИЕ")
print_matrix("Q", Q_g)
print_matrix("R", R_g)

print_vector("x (через QR)", x_g_qr)

if is_positive_definite(A_g):
    L_chol_g, x_g_chol = solve_by_cholesky(A_g, b_g)

    print("РАЗЛОЖЕНИЕ ХОЛЕЦКОГО")
    print_matrix("L", L_chol_g)
    print_vector("x (через Холецкого)", x_g_chol)
else:
    print("Разложение Холецкого для системы г) не применяется.")