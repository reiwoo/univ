import numpy as np
from time import perf_counter

def dense_matvec(A, x):
    n = len(x)
    result = np.zeros(n, dtype=float)

    for i in range(n):
        total = 0.0
        for j in range(n):
            total += A[i, j] * x[j]
        result[i] = total
    return result

def csr_from_dense(A):
    n = A.shape[0]
    values = []
    col_indices = []
    row_ptr = [0]

    for i in range(n):
        for j in range(n):
            if A[i, j] != 0:
                values.append(A[i, j])
                col_indices.append(j)
        row_ptr.append(len(values))

    return (np.asarray(values, dtype=float), np.asarray(col_indices, dtype=int), np.asarray(row_ptr, dtype=int))

def csr_matvec(values, col_indices, row_ptr, x):
    n = len(row_ptr) - 1
    result = np.zeros(n, dtype=float)

    for i in range(n):
        for k in range(row_ptr[i], row_ptr[i + 1]):
            result[i] += values[k] * x[col_indices[k]]
    return result

def csir_from_dense(A):
    n = A.shape[0]
    diagonal = np.diag(A).copy()

    lower_values = []
    upper_values = []
    col_indices = []
    row_ptr = [0]

    for i in range(n):
        for j in range(i):
            if A[i, j] != 0 or A[j, i] != 0:
                lower_values.append(A[i, j])
                upper_values.append(A[j, i])
                col_indices.append(j)
        row_ptr.append(len(lower_values))

    return (diagonal, np.asarray(lower_values, dtype=float), np.asarray(upper_values, dtype=float), np.asarray(col_indices, dtype=int), np.asarray(row_ptr, dtype=int))

def csir_matvec(diagonal, lower_values, upper_values, col_indices, row_ptr, x):
    n = len(diagonal)
    result = diagonal * x

    for i in range(n):
        for k in range(row_ptr[i], row_ptr[i + 1]):
            j = col_indices[k]
            result[i] += lower_values[k] * x[j]
            result[j] += upper_values[k] * x[i]
    return result

def make_unsymmetric_matrix(n, density, rng):
    mask = rng.random((n, n)) < density
    A = rng.uniform(-10.0, 10.0, size=(n, n)) * mask
    A[np.diag_indices(n)] = rng.uniform(1.0, 10.0, size=n)

    return A

def make_symmetric_pattern_matrix(n, density, rng):
    A = np.zeros((n, n), dtype=float)
    A[np.diag_indices(n)] = rng.uniform(1.0, 10.0, size=n)

    rows, cols = np.tril_indices(n, k=-1)
    selected = rng.random(len(rows)) < density

    rows = rows[selected]
    cols = cols[selected]

    A[rows, cols] = rng.uniform(-10.0, 10.0, size=len(rows))
    A[cols, rows] = rng.uniform(-10.0, 10.0, size=len(rows))

    return A

def benchmark(function, repeats=3, number=3):
    times = []

    for _ in range(repeats):
        start = perf_counter()
        for _ in range(number):
            function()

        times.append((perf_counter() - start) / number)
    return min(times)

sizes = [100, 300, 600, 900]
density = 0.02
rng = np.random.default_rng(42)

for n in sizes:
    x = rng.uniform(-5.0, 5.0, size=n)
    A_csr = make_unsymmetric_matrix(n, density, rng)
    values, col_indices, row_ptr = csr_from_dense(A_csr)
    result_csr = csr_matvec(values, col_indices, row_ptr, x)
    expected_csr = A_csr @ x

    if not np.allclose(result_csr, expected_csr):
        raise AssertionError(f"Ошибка CSR при n={n}")

    dense_time_csr = benchmark(lambda: dense_matvec(A_csr, x))
    csr_time = benchmark(lambda: csr_matvec(values, col_indices, row_ptr, x))

    A_csir = make_symmetric_pattern_matrix(n, density, rng)
    diagonal, lower_values, upper_values, csir_cols, csir_ptr = csir_from_dense(A_csir)
    result_csir = csir_matvec(diagonal, lower_values, upper_values, csir_cols, csir_ptr, x)
    expected_csir = A_csir @ x

    if not np.allclose(result_csir, expected_csir):
        raise AssertionError(f"Ошибка CSIR при n={n}")

    dense_time_csir = benchmark(lambda: dense_matvec(A_csir, x))
    csir_time = benchmark(lambda: csir_matvec(diagonal, lower_values, upper_values, csir_cols, csir_ptr, x))

    print(f"Размерность n = {n}")
    print(
        f"  CSR: ненулевых элементов = {len(values)}, "
        f"плотная матрица = {dense_time_csr * 1000:.3f} мс, "
        f"CSR = {csr_time * 1000:.3f} мс"
    )

    csir_nnz = n + len(lower_values) + len(upper_values)

    print(
        f"  CSIR: хранимых элементов = {csir_nnz}, "
        f"плотная матрица = {dense_time_csir * 1000:.3f} мс, "
        f"CSIR = {csir_time * 1000:.3f} мс"
    )
    print()