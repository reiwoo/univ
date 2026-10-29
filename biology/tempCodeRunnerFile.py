Ai = tau * D1 / h**2
Ci = 2*tau*D1 / h**2+1
Bi = tau * D1 / h**2

for j in range(1, M):
    alpha[0] = 1.0
    beta[0]  = 0.0
    for i in range(1, M):
        Fi = u1[j-1, i] + tau * f1(u1[j-1, i], u3[j-1, i], (j-1)*tau)
        lower = Ci - Ai * alpha[i-1]
        alpha[i] = Bi / lower
        beta[i]  = (Fi + Ai * beta[i-1]) / lower
    u1[j, N] = beta[N] / (1 - alpha[N])
    for i in range(N-1, -1, -1):
        u1[j, i] = alpha[i] * u1[j, i+1] + beta[i]

Ai = tau * D1 / h**2
Ci = 2*tau*D1 / h**2+1
Bi = tau * D1 / h**2
alpha[0] = 1.0
beta[0]  = 0.0
for i in range(1, N):
    Fi = u2[j-1, i] + tau * f2(u1[j-1, i], u2[j-1, i], u3[j-1, i])
    lower = Ci - Ai * alpha[i-1]
    alpha[i] = Bi / lower
    beta[i]  = (Fi + Ai * beta[i-1]) / lower
u2[j, N] = beta[N] / (1 - alpha[N])
for i in range(N-1, 0, -1):
    u2[j, i] = alpha[i] * u2[j][i+1] + beta[i]
for i in range(1, N):
    u3[j, i] = u3[j-1][i] + tau * f3(u1[j-1][i], u2[j-1][i], u3[j-1][i], (j-1)*tau)