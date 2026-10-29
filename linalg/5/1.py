import time
import numpy as np
import scipy.sparse as sp

# ---------------------------------------------------------------
# Форматы хранения
# ---------------------------------------------------------------
def dense_to_csr(A):
    """CSR: val - значения, col - номера столбцов, ptr - начала строк (длина n+1)."""
    n = A.shape[0]
    val, col, ptr = [], [], [0]
    for i in range(n):
        nz = np.nonzero(A[i])[0]
        val.extend(A[i, nz]); col.extend(nz)
        ptr.append(len(val))
    return np.array(val), np.array(col, dtype=int), np.array(ptr, dtype=int)

def dense_to_cslr(A):
    """CSlR (симметричный портрет, ненулевая диагональ):
       di  - диагональ,
       ig  - начала строк нижнего треугольника (длина n+1),
       jg  - столбцы нижнего треугольника,
       ggl - значения нижнего треугольника,
       ggu - значения верхнего треугольника (тот же портрет, транспонированный)."""
    n = A.shape[0]
    di = np.diag(A).copy()
    ig, jg, ggl, ggu = [0], [], [], []
    for i in range(n):
        for j in np.nonzero(A[i, :i])[0]:
            jg.append(j); ggl.append(A[i, j]); ggu.append(A[j, i])
        ig.append(len(jg))
    return di, np.array(ig), np.array(jg, dtype=int), np.array(ggl), np.array(ggu)

# ---------------------------------------------------------------
# Умножение матрицы на вектор (чистый Python, списки — честное сравнение)
# ---------------------------------------------------------------
def matvec_dense(A, x):
    n = len(x)
    y = [0.0] * n
    for i in range(n):
        s = 0.0
        row = A[i]
        for j in range(n):
            s += row[j] * x[j]
        y[i] = s
    return y

def matvec_csr(val, col, ptr, x):
    n = len(ptr) - 1
    y = [0.0] * n
    for i in range(n):
        s = 0.0
        for k in range(ptr[i], ptr[i + 1]):
            s += val[k] * x[col[k]]
        y[i] = s
    return y

def matvec_cslr(di, ig, jg, ggl, ggu, x):
    n = len(di)
    y = [di[i] * x[i] for i in range(n)]
    for i in range(n):
        xi = x[i]
        s = 0.0
        for k in range(ig[i], ig[i + 1]):
            j = jg[k]
            s += ggl[k] * x[j]       # элемент a[i, j] нижнего треугольника
            y[j] += ggu[k] * xi      # элемент a[j, i] верхнего треугольника
        y[i] += s
    return y

# Векторизованные варианты (numpy) — для справки
def matvec_csr_np(val, col, rows, x, n):
    return np.bincount(rows, weights=val * x[col], minlength=n)

def matvec_cslr_np(di, jg, rows_l, ggl, ggu, x, n):
    return (di * x + np.bincount(rows_l, weights=ggl * x[jg], minlength=n)
                   + np.bincount(jg, weights=ggu * x[rows_l], minlength=n))

# ---------------------------------------------------------------
# Генерация тестовых матриц
# ---------------------------------------------------------------
def gen_nonsym(n, per_row, rng):
    """Разреженная несимметричная матрица (~per_row ненулей на строку)."""
    A = np.zeros((n, n))
    m = n * per_row
    A[rng.integers(0, n, m), rng.integers(0, n, m)] = rng.uniform(-1, 1, m)
    return A

def gen_sym_portrait(n, per_row, rng):
    """Симметричный портрет, ненулевая диагональ, значения несимметричны."""
    A = np.zeros((n, n))
    m = n * per_row // 2
    i = rng.integers(0, n, m); j = rng.integers(0, n, m)
    mask = i != j
    i, j = i[mask], j[mask]
    A[i, j] = rng.uniform(-1, 1, len(i))
    A[j, i] = rng.uniform(-1, 1, len(i))
    A[np.arange(n), np.arange(n)] = rng.uniform(1, 2, n)
    return A

def best_time(f, min_total=0.2):
    f()
    reps, t = 1, 0.0
    while True:
        t0 = time.perf_counter()
        for _ in range(reps):
            f()
        t = time.perf_counter() - t0
        if t >= min_total:
            return t / reps
        reps *= 4

def run(sizes=(100, 200, 500, 1000, 2000), per_row=5, seed=0):
    rng = np.random.default_rng(seed)
    for kind, gen in [("CSR  (несимметричная)", gen_nonsym),
                      ("CSlR (симметричный портрет)", gen_sym_portrait)]:
        print(f"\n=== {kind}, ~{per_row} ненулей в строке ===")
        print(f"{'n':>5s} {'nnz':>6s} {'fill,%':>7s} {'ошибка':>9s} | "
              f"{'dense,мс':>9s} {'sparse,мс':>9s} {'ускор.':>7s} | "
              f"{'numpy dense':>11s} {'numpy sp':>9s} {'scipy':>7s} | {'память dense/sparse'}")
        for n in sizes:
            A = gen(n, per_row, rng)
            x = rng.standard_normal(n)
            y_ref = A @ x
            Al, xl = A.tolist(), x.tolist()
            nnz = np.count_nonzero(A)
            if kind.startswith("CSR"):
                val, col, ptr = dense_to_csr(A)
                rows = np.repeat(np.arange(n), np.diff(ptr))
                f_sp = lambda: matvec_csr(val, col, ptr, xl)
                f_np = lambda: matvec_csr_np(val, col, rows, x, n)
                mem_sp = val.nbytes + col.nbytes + ptr.nbytes
                y_sp = np.array(f_sp())
            else:
                di, ig, jg, ggl, ggu = dense_to_cslr(A)
                rows_l = np.repeat(np.arange(n), np.diff(ig))
                f_sp = lambda: matvec_cslr(di, ig, jg, ggl, ggu, xl)
                f_np = lambda: matvec_cslr_np(di, jg, rows_l, ggl, ggu, x, n)
                mem_sp = sum(a.nbytes for a in (di, ig, jg, ggl, ggu))
                y_sp = np.array(f_sp())
            err = np.linalg.norm(y_sp - y_ref) / np.linalg.norm(y_ref)
            S = sp.csr_matrix(A)
            t_d  = best_time(lambda: matvec_dense(Al, xl))
            t_s  = best_time(f_sp)
            t_nd = best_time(lambda: A @ x)
            t_ns = best_time(f_np)
            t_sc = best_time(lambda: S @ x)
            print(f"{n:5d} {nnz:6d} {100*nnz/n/n:7.2f} {err:9.1e} | "
                  f"{t_d*1e3:9.3f} {t_s*1e3:9.3f} {t_d/t_s:7.1f} | "
                  f"{t_nd*1e6:9.1f}мкс {t_ns*1e6:7.1f}мкс {t_sc*1e6:5.1f}мкс | "
                  f"{A.nbytes/1024:.0f} / {mem_sp/1024:.0f} КБ")

if __name__ == "__main__":
    run()