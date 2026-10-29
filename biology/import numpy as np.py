import numpy as np
import matplotlib.pyplot as plt

gamma1, gamma2, gamma3 = 0.2, 0.1, 0.2
mu1, mu2 = 1.4, 1.4
D1 = 0.001 * mu1
D2 = 0.0000001 * mu2

def g1(t): return 0.002 * t
def g3(t): return 0.005 * t

def f1(u1, u3, t):
    return mu1*u1 - mu1*u1*u3 - gamma1*u1*u3 - g1(t)*u1
def f2(u1, u2, u3):
    return mu2*u2*(1 - u2) - mu2*u2*u3 - gamma2*u1*u2 - gamma3*u2*u3

L, T = 1.0, 40.0
N, M = 1000, 1000
h, tau = L/N, T/M
u1 = np.zeros((M+1, N+1))
u2 = np.zeros((M+1, N+1))
u3 = np.zeros((M+1, N+1))
alpha = np.zeros(N+1)
beta = np.zeros(N+1)

for i in range(N-1):
    u1[0][i] = 0.1
    u2[0][i] = 1.0
    u3[0][i] = 0.0

for j in range(1, M+1):
    t = j * tau

    A = tau * D1 / h**2
    C = 1 + 2*A
    alpha[0], beta[0] = 1.0, 0.0
    for i in range(1, N):
        Fi = u1[j-1, i] + tau * f1(u1[j-1, i], u3[j-1, i], t)
        denom = C - A*alpha[i-1]
        alpha[i] = A / denom
        beta[i] = (Fi + A*beta[i-1]) / denom
    u1[j, N] = beta[N-1] / (1 - alpha[N-1])
    for i in range(N-1, -1, -1):
        u1[j, i] = alpha[i]*u1[j, i+1] + beta[i]

    A = tau * D2 / h**2
    C = 1 + 2*A
    alpha[0], beta[0] = 1.0, 0.0
    for i in range(1, N):
        Fi = u2[j-1, i] + tau * f2(u1[j, i], u2[j-1, i], u3[j-1, i])
        denom = C - A*alpha[i-1]
        alpha[i] = A / denom
        beta[i] = (Fi + A*beta[i-1]) / denom
    u2[j, N] = beta[N-1] / (1 - alpha[N-1])
    for i in range(N-1, -1, -1):
        u2[j, i] = alpha[i]*u2[j, i+1] + beta[i]

    for i in range(N+1):
        R = (gamma2 * u1[j, i] * u2[j, i] + 
             gamma1 * u1[j, i] * u3[j-1, i] + 
             gamma3 * u2[j, i] * u3[j-1, i])
        
        numerator = u3[j-1, i] + tau * R * (1 - u3[j-1, i])
        denominator = 1 + tau * g3(t)
        u3[j, i] = numerator / denominator

x = [i*h for i in range(N+1)]
plt.figure()
plt.xlabel("x")
plt.ylabel("u")
plt.plot(x, u1, color="yellow")
plt.plot(x, u2, color="green")
plt.plot(x, u3, color="cyan")
plt.grid()
plt.show()