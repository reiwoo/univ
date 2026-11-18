import numpy as np
import scipy.linalg as la

A_sp = np.array([[16, 2, 3, 4],
                 [2, 16, 3, 4],
                 [3, 3, 16, 2],
                 [4, 4, 2, 16]])

def sp_algorithm(A, eps=1e-10, max_iter=10000):
    n = A.shape[0]
    y = np.ones(n)
    x = y / np.linalg.norm(y)                       # шаги 1-2
    lambda0 = 0.0
    for k in range(1, max_iter + 1):
        y = A @ x                                   # шаг 3
        s = y @ y                                   # шаг 4
        t = y @ x
        lam = s / t
        x = y / np.sqrt(s)
        if abs(lam - lambda0) <= eps:              # шаг 5
            return lam, x, k
        lambda0 = lam
    return lam, x, max_iter

def reference(A):
    eigenvalues, eigenvectors = la.eig(A)
    max_idx = 0
    max_val = abs(eigenvalues[0])
    for i in range(1, len(eigenvalues)):
        if abs(eigenvalues[i]) > max_val:
            max_val = abs(eigenvalues[i])
            max_idx = i
    return eigenvalues, eigenvalues[max_idx], eigenvectors[:, max_idx]

lam, x, k = sp_algorithm(A_sp)
w, lambdamax_ref, x_ref = reference(A_sp)
x_ref = np.real(x_ref)
x_ref /= np.linalg.norm(x_ref)

print(f"Eig (SP):      lambda_max  = {lam:.10f}, (it: {k})")
print(f"Eig (scipy):   lambda_max = {lambdamax_ref.real:.10f}")
print("Vector (SP):  ", np.round(x, 8))
print("Vector (Scipy): ", np.round(x_ref, 8))
print(f"|lambda - lambda_eig| = {abs(lam - lambdamax_ref.real):.2e},  ||x - x_eig|| = {np.linalg.norm(x - x_ref):.2e}")
print(f"||Ax - lambda x|| = {np.linalg.norm(A_sp @ x - lam * x):.2e}\n")