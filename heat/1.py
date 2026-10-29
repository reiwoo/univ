import numpy as np
import matplotlib.pyplot as plt

rho = 920.0           
cp_ice = 2100.0        
cp_water = 4200.0      
lam_ice = 2.21          
lam_water = 0.6         
L_fusion = 334000.0  

L = 1.0
alpha1 = 50.0         
alpha2 = 5e-3
T_left = 50.0         
T_right = -10.0       
T0 = -10.0             

T_phase = 0.0          
dT_smooth = 1.0         

n = 200               
dx = L / n
x = np.linspace(0, L, n + 1)

total_time = 20 * 3600 
dt = 5.0               
n_steps = int(total_time / dt)

def progonka(a, b, c, d):
    n_len = len(d)
    cp = np.zeros(n_len - 1)
    dp = np.zeros(n_len)
    
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    
    for i in range(1, n_len - 1):
        denom = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / denom
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom
        
    x_sol = np.zeros(n_len)
    x_sol[n_len - 1] = (d[n_len - 1] - a[n_len - 1] * dp[n_len - 2]) / (b[n_len - 1] - a[n_len - 1] * cp[n_len - 2])
    
    for i in range(n_len - 2, -1, -1):
        x_sol[i] = dp[i] - cp[i] * x_sol[i + 1]
        
    return x_sol

def get_properties(T_arr):
    Cp_vol = np.zeros_like(T_arr)
    Lam = np.zeros_like(T_arr)
    
    for i, t_val in enumerate(T_arr):
        if (t_val >= T_phase - dT_smooth) and (t_val <= T_phase + dT_smooth):
            cp_eff = (cp_ice + cp_water)/2.0 + L_fusion / (2 * dT_smooth)
            Cp_vol[i] = rho * cp_eff
            Lam[i] = (lam_ice + lam_water) / 2.0
            
        elif t_val < T_phase - dT_smooth:
            Cp_vol[i] = rho * cp_ice
            Lam[i] = lam_ice
            
        else:
            Cp_vol[i] = rho * cp_water
            Lam[i] = lam_water
            
    return Cp_vol, Lam

T = np.full(n + 1, T0)
save_times_h = [1, 5, 10, 15, 20]    
save_steps = [int(t * 3600 / dt) for t in save_times_h]
T_history = []
labels = []

for step in range(n_steps + 1):
    if step in save_steps:
        T_history.append(T.copy())
        labels.append(f"{step * dt / 3600:.1f} ч")
    Cp_vol_current, Lam_current = get_properties(T)
    r = Lam_current * dt / (Cp_vol_current * dx**2)

    a = np.zeros(n + 1)
    b = np.zeros(n + 1)
    c = np.zeros(n + 1)
    d = np.zeros(n + 1)

    for i in range(1, n):
        a[i] = -r[i]
        b[i] = 1 + 2 * r[i]
        c[i] = -r[i]
        d[i] = T[i]

    coeff_left = 2 * r[0] * dx * alpha1 / Lam_current[0]
    b[0] = 1 + 2 * r[0] + coeff_left
    c[0] = -2 * r[0]
    d[0] = T[0] + coeff_left * T_left
    a[0] = 0.0

    coeff_right = 2 * r[n] * dx * alpha2 / Lam_current[n]
    a[n] = -2 * r[n]
    b[n] = 1 + 2 * r[n] + coeff_right
    d[n] = T[n] + coeff_right * T_right
    c[n] = 0.0

    T = thomas(a, b, c, d)
plt.figure(figsize=(10, 6))

for i in range(len(T_history)):
    plt.plot(x, T_history[i], linewidth=2, label=labels[i])
plt.axhline(0, color='black', linestyle='--', alpha=0.5, label="0°C (Плавление)")

plt.xlabel("Координата x, м", fontsize=12)
plt.ylabel("Температура T, °C", fontsize=12)
plt.title("Таяние льда (Задача Стефана)", fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()