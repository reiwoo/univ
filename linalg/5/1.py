import time
import numpy as np
import scipy.sparse as sp

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


def matvec_csr_np(val, col, rows, x, n):
    return np.bincount(rows, weights=val * x[col], minlength=n)

def matvec_cslr_np(di, jg, rows_l, ggl, ggu, x, n):
    return (di * x + np.bincount(rows_l, weights=ggl * x[jg], minlength=n)
                   + np.bincount(jg, weights=ggu * x[rows_l], minlength=n))


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
    print("Время умножения матрицы на вектор, мс")
    print(f"{'n':>5s} | {'плотная':>8s} {'CSR':>7s} {'выигрыш':>8s} | "
          f"{'плотная':>8s} {'CSlR':>7s} {'выигрыш':>8s}")
    for n in sizes:
        x = rng.standard_normal(n)
        xl = x.tolist()
        res = []
        for gen, to_fmt, mv in [(gen_nonsym, dense_to_csr, matvec_csr),
                                (gen_sym_portrait, dense_to_cslr, matvec_cslr)]:
            A = gen(n, per_row, rng)
            fmt = to_fmt(A)
            Al = A.tolist()

            assert np.allclose(mv(*fmt, xl), A @ x), "ошибка умножения"
            t_d = best_time(lambda: matvec_dense(Al, xl))
            t_s = best_time(lambda: mv(*fmt, xl))
            res += [t_d * 1e3, t_s * 1e3, t_d / t_s]
        print(f"{n:5d} | {res[0]:8.3f} {res[1]:7.3f} {res[2]:7.1f}x | "
              f"{res[3]:8.3f} {res[4]:7.3f} {res[5]:7.1f}x")

if __name__ == "__main__":
    run()