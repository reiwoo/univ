import numpy as np
import matplotlib.pyplot as plt
from math import *

gamma1 = 0.2
gamma2 = 0.1
gamma3 = 0.2
mu1 = 1.4
mu2 = 1.4
D1 = 0.001 * mu1
D2 = 0.0000001 * mu2   


def f1(u1, u3, t):
    return mu1 * u1 * (1 - u3) - gamma1 * u1 * u3 - phi1(t) * u1
def f2(u1, u2, u3):
    return mu2 * u2 * (1 - u2 - u3) - (gamma2 * u1 * u2 + gamma3 * u2 * u3)
def f3(u1, u2, u3, t):
    return (gamma2 * u1 * u2 + gamma1 * u1 * u3 + gamma3 * u2 * u3) * (1 - u3) - phi3(t) * u3
def phi1(t):
    return t * 0.002
def phi3(t):
    return t * 0.005

l=3
T=40
N=1000
M=1000
h=l/N
tau=T/M
u1 = np.zeros((M+1, N+1))
u2 = np.zeros((M+1, N+1))
u3 = np.zeros((M+1, N+1))
alpha=np.zeros(N+1)
beta=np.zeros(N+1)

for i in range(N-1):
    u1[0][i] = 0.1
    u2[0][i] = 1.0
    u3[0][i] = 0.0

Ai = tau * D1 / h**2
Ci = 2*tau*D1 / h**2+1
Bi = tau * D1 / h**2
for j in range(1, M):
    alpha[0] = 1.0
    beta[0]  = 0.0
    for i in range(1, N):
        Fi = u1[j-1][i] + tau * f1(u1[j-1][i], u3[j-1][i], (j-1)*tau)
        lower = Ci-Ai*alpha[i-1]
        alpha[i] = Bi / lower
        beta[i]  = (Fi + Ai*beta[i-1])/lower
    u1[j][N] = beta[N]/(1.0-alpha[N])
    for i in range(N-1, -1, -1):
        u1[j][i] = alpha[i]*u1[j][i+1]+beta[i]
        
        
    Ai = tau*D2/h**2
    Ci = 2*tau*D2/h**2+1
    Bi = tau*D2/h**2
    alpha[0] = 1.0
    beta[0]  = 0.0
    for i in range(1, N):
        Fi = u2[j-1][i]+tau*f2(u1[j-1][i], u2[j-1][i], u3[j-1][i])
        lower = Ci-Ai*alpha[i-1]
        alpha[i] = Bi/lower
        beta[i]  = (Fi+Ai*beta[i-1])/lower
    u2[j][N] = beta[N]/(1.0-alpha[N])
    for i in range(N-1, -1, -1):
        u2[j][i] = alpha[i]*u2[j][i+1]+beta[i]
        
    for i in range(1, N):
        u3[j][i] = u3[j-1][i]+tau*f3(u1[j-1][i], u2[j-1][i], u3[j-1][i], (j-1)*tau)

x = [i*h for i in range(N+1)]
plt.figure()
plt.xlabel("x")
plt.ylabel("u")
plt.plot(x, u1, color="yellow")
plt.plot(x, u2, color="green")
plt.plot(x, u3, color="cyan")
plt.grid()
plt.show()