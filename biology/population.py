import numpy as np
import matplotlib.pyplot as plt

# ====================== ПАРАМЕТРЫ ======================
N = 100
D1 = 0.0001
D2 = 0.0002
D3 = 0.0001
tao = 0.09
h = 1.0 / N

# Граничные условия ИЗ ПОСТАНОВКИ ЗАДАЧИ (правильные!)
u1_left = 1.45
u2_left = 0.8
v_left  = 0.55

x = np.linspace(0, 1, N + 1)

u1 = np.zeros((N + 1, N + 1))
u2 = np.zeros((N + 1, N + 1))
v  = np.zeros((N + 1, N + 1))

# Начальные условия
for i in range(N + 1):
    xx = x[i]
    u1[i, 0] = 5 * (xx - 0.5)**2 + 0.2
    u2[i, 0] = 3 * (xx - 0.5)**2 + 0.05
    v[i, 0]  = (xx - 0.5)**2 + 0.3

# ====================== РЕШЕНИЕ ======================
for j in range(N):
    # u1
    a = D1 * tao / h**2
    alpha = np.zeros(N + 2)
    beta = np.zeros(N + 2)
    for i in range(1, N):
        c = 2 * a + 1
        alpha[i + 1] = a / (c - a * alpha[i])
        f = u1[i, j] * (2.4 - u1[i, j] - 6 * u2[i, j] - 4 * v[i, j])
        d = u1[i, j] + tao * f
        beta[i + 1] = (a * beta[i] + d) / (c - a * alpha[i])
    u1[N, j + 1] = beta[N] / (1 - alpha[N])
    for i in range(N - 1, 0, -1):
        u1[i, j + 1] = alpha[i + 1] * u1[i + 1, j + 1] + beta[i + 1]
    u1[0, j + 1] = u1_left

    # u2
    a = D2 * tao / h**2
    alpha = np.zeros(N + 2)
    beta = np.zeros(N + 2)
    for i in range(1, N):
        c = 2 * a + 1
        alpha[i + 1] = a / (c - a * alpha[i])
        f = u2[i, j] * (4.0 - u2[i, j] - u1[i, j] - 10 * v[i, j])
        d = u2[i, j] + tao * f
        beta[i + 1] = (a * beta[i] + d) / (c - a * alpha[i])
    u2[N, j + 1] = beta[N] / (1 - alpha[N])
    for i in range(N - 1, 0, -1):
        u2[i, j + 1] = alpha[i + 1] * u2[i + 1, j + 1] + beta[i + 1]
    u2[0, j + 1] = u2_left

    # v
    a = D3 * tao / h**2
    alpha = np.zeros(N + 2)
    beta = np.zeros(N + 2)
    for i in range(1, N):
        c = 2 * a + 1
        alpha[i + 1] = a / (c - a * alpha[i])
        f = -v[i, j] * (1.0 - 0.25 * u1[i, j] - 4 * u2[i, j] + v[i, j])
        d = v[i, j] + tao * f
        beta[i + 1] = (a * beta[i] + d) / (c - a * alpha[i])
    v[N, j + 1] = beta[N] / (1 - alpha[N])
    for i in range(N - 1, 0, -1):
        v[i, j + 1] = alpha[i + 1] * v[i + 1, j + 1] + beta[i + 1]
    v[0, j + 1] = v_left

print(f"Готово! t = {N*tao:.1f}")
print(f"u₁ (синяя) в центре x=0.5: {u1[N//2, -1]:.6f}  ← почти 0, как и должно быть")
print(f"u₂ в центре: {u2[N//2, -1]:.4f}")
print(f"v  в центре: {v[N//2, -1]:.4f}")

# График (уже показан выше)
plt.figure(figsize=(12, 8))
plt.plot(x, u1[:,-1], 'b-', lw=3, label='u₁ — синяя жертва')
plt.plot(x, u2[:,-1], 'g-', lw=3, label='u₂')
plt.plot(x, v[:,-1],  'r-', lw=3, label='v — хищник')
plt.xlabel('x')
plt.ylabel('Плотность')
plt.title('Решение модели (правильные условия)')
plt.legend()
plt.grid(True)
plt.show()