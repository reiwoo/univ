import numpy as np
from time import perf_counter

rng = np.random.default_rng(0)
np.set_printoptions(precision=1, suppress=True, linewidth=150)

def dense_matvec(A, x):
    n = len(x)
    y = np.zeros(n)
    for i in range(n):
        for j in range(n):
            y[i] += A[i, j] * x[j]
    return y

def CSR_from_dense(A):
    n = A.shape[0]
    values, cols, ptr = [], [], [0]
    for i in range(n):
        for j in range(n):
            if A[i, j] != 0:
                values.append(A[i, j])
                cols.append(j)
        ptr.append(len(values))
    return np.array(values), np.array(cols), np.array(ptr)

def CSR_matvec(values, cols, ptr, x):
    n = len(ptr) - 1
    y = np.zeros(n)
    for i in range(n):
        for k in range(ptr[i], ptr[i + 1]):
            y[i] += values[k] * x[cols[k]]
    return y

def CSlR_from_dense(A):
    n = A.shape[0]
    diag = np.diag(A).copy()
    lower, upper, cols, ptr = [], [], [], [0]
    for i in range(n):
        for j in range(i):
            if A[i, j] != 0 or A[j, i] != 0:
                lower.append(A[i, j])
                upper.append(A[j, i])
                cols.append(j)
        ptr.append(len(lower))
    return diag, np.array(lower), np.array(upper), np.array(cols), np.array(ptr)

def CSlR_matvec(diag, lower, upper, cols, ptr, x):
    n = len(diag)
    y = diag * x
    for i in range(n):
        for k in range(ptr[i], ptr[i + 1]):
            j = cols[k]
            y[i] += lower[k] * x[j]
            y[j] += upper[k] * x[i]
    return y

def make_matrix(n, density, rng):
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if rng.random() < density:
                A[i, j] = rng.uniform(-5, 5)
    for i in range(n):
        A[i, i] = rng.uniform(1, 5)
    return A

def make_sym_portrait_matrix(n, density, rng):
    A = np.zeros((n, n))
    for i in range(n):
        A[i, i] = rng.uniform(1, 5)
    for i in range(n):
        for j in range(i):
            if rng.random() < density:
                val = rng.uniform(-5, 5)
                A[i, j] = val
                A[j, i] = val
    return A

def timer(f, repeats=3):
    times = []
    for _ in range(repeats):
        t = perf_counter()
        f()
        times.append(perf_counter() - t)
    return min(times) * 1000

for n in [10, 100, 300, 600, 900]:
    density = 0.1 if n == 10 else 0.02
    x = rng.uniform(-5, 5, n)
    A = make_matrix(n, density, rng)
    CSR = CSR_from_dense(A)
    assert np.allclose(CSR_matvec(*CSR, x), A @ x)

    B = make_sym_portrait_matrix(n, density, rng)
    CSlR = CSlR_from_dense(B)
    assert np.allclose(CSlR_matvec(*CSlR, x), B @ x)

    if n == 10:
        print("Матрица A (несимметричная):")
        print(A)
        print("CSR: values =", CSR[0])
        print("     cols   =", CSR[1])
        print("     ptr    =", CSR[2])
        print("\nМатрица B (симметричный портрет):")
        print(B)
        print("CSlR: diag  =", CSlR[0])
        print("      lower =", CSlR[1])
        print("      upper =", CSlR[2])
        print("      cols  =", CSlR[3])
        print("      ptr   =", CSlR[4])
        print()

    print(f"n = {n}")
    print(f"  CSR:  обычная = {timer(lambda: dense_matvec(A, x)):.3f} мс, "
          f"CSR = {timer(lambda: CSR_matvec(*CSR, x)):.3f} мс")
    print(f"  CSlR: обычная = {timer(lambda: dense_matvec(B, x)):.3f} мс, "
          f"CSlR = {timer(lambda: CSlR_matvec(*CSlR, x)):.3f} мс")
    print()