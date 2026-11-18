import numpy as np
import scipy.linalg as la

def pm_algorithm(A, eps=1e-10, max_iter=10000):
    n = A.shape[0]
    y = np.ones(n)
    x = y / np.linalg.norm(y)                       # шаг 1
    lambda0 = 0.0
    for k in range(1, max_iter + 1):
        y = A @ x                                   # шаг 2
        x_new = y / np.linalg.norm(y)               # шаг 3
        total = 0.0
        count = 0
        for i in range(n):                          # шаг 4
            if abs(x[i]) > eps:
                total += y[i] / x[i]
                count += 1
        lam = total / count
        x = x_new
        if abs(lam - lambda0) < eps:               # шаг 5
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

matrices = {
    "1a": np.array([[8, 1, 3], 
                    [2, 10, 0], 
                    [1, 1, 12]]),
                    
    "1b": np.array([[10, 0, 2, 5, 0],
                    [2, 1, 0, 4, 0],
                    [3, 0, 4, 1, 0],
                    [0, 2, 4, 2, 0],
                    [3, 0, 0, 1, 1]])
}

for name, A in matrices.items():
    lam, x, k = pm_algorithm(A)
    eigenvalues, lambdamax_ref, x_ref = reference(A)
    x_ref = np.real(x_ref)
    x_ref /= np.linalg.norm(x_ref)
        
    print(f"Eig (PM):      lambda_max = {lam:.10f}  (it: {k})")
    print(f"Eig (scipy):   lambda_max = {lambdamax_ref.real:.10f}")
    print("Vector (PM):  ", np.round(x, 8))
    print("Vector (Scipy): ", np.round(x_ref, 8))
    print(f"Diff:            {abs(lam - lambdamax_ref.real):.2e}")
    print(f"Diff Vector (norm):    {np.linalg.norm(x - x_ref):.2e}")
    print(f"||Ax - lambda*x||:    {np.linalg.norm(A @ x - lam * x):.2e}\n")