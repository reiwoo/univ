import numpy as np
import matplotlib.pyplot as plt

l = 5.0          
N = 5000        
h = l / N      
x_grid = np.linspace(0, l, N + 1)

# Фаза 1 (Лед)
lambda_1 = 2.21
rho_1 = 920.0
c_1 = 1900.0
# Фаза 2 (Вода)
lambda_2 = 0.58
rho_2 = 1000.0
c_2 = 4200.0

L_lat = 3.34e5   # Удельная теплота плавления
myu_1 = -1.02    # Левая граница (Лед)
myu_2 = 4.0      # Правая граница (Вода)
u_0_val = 4.0    # Начальная температура поля

u = np.full(N + 1, u_0_val, dtype=float)
u[0] = myu_1

r1_const = (c_1 * rho_1 * h**2) / lambda_1
r2_const = (c_2 * rho_2 * h**2) / lambda_2

# -------------------- Метод Прогонки --------------------
def tdma_solve(a, b, c, d):
    n = len(d)
    ac, bc, cc, dc = map(np.array, (a, b, c, d)) 
    for i in range(1, n):
        m = ac[i] / bc[i-1]
        bc[i] = bc[i] - m * cc[i-1]
        dc[i] = dc[i] - m * dc[i-1]
    x = np.zeros(n)
    x[-1] = dc[-1] / bc[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (dc[i] - cc[i] * x[i+1]) / bc[i]
    return x

# -------------------- ЦИКЛ --------------------
# j - индекс узла, где находится фронт фазового перехода.
# Фронт движется от x[1] до x[N-1]
time = 0.0
time_history = [0.0]
front_history = [0.0] # Фронт стартует из 0 (по условию u(0)=myu_1, u(x)=4, скачок в 0)

u[0] = myu_1
u[1:] = u_0_val

j = 1 

T_max = 210.0 * 86400.0 

results_to_plot = []

print(f"{'Step (j)':<10} | {'Time (days)':<15} | {'Tau (s)':<15} | {'Front (m)':<10}")

while j < N and time < T_max:
    
    # Фаза 1 (Лед)
    n1 = j - 1
    if n1 > 0:
        a1 = np.ones(n1) 
        b1 = -(2.0 + r1_const) * np.ones(n1) 
        c1 = np.ones(n1) 
        d1 = -r1_const * u[1:j]
        d1[0] -= myu_1  # v_0 = myu_1
        d1[-1] -= 0.0   # v_j = 0
        
        if n1 == 1: 
             v_phase1 = np.array([d1[0]/b1[0]])
        else:
             a1[0] = 0 
             c1[-1] = 0
             v_phase1 = tdma_solve(a1, b1, c1, d1)
    else:
        v_phase1 = np.array([])

    # Фаза 2 (Вода)
    n2 = (N - 1) - (j + 1) + 1
    
    if n2 > 0:
        a2 = np.ones(n2)
        b2 = -(2.0 + r2_const) * np.ones(n2)
        c2 = np.ones(n2)
        d2 = -r2_const * u[j+1:N]
        
        # ГУ слева для фазы 2
        d2[0] -= 0.0
        # ГУ справа для фазы 2
        d2[-1] -= myu_2
        
        if n2 == 1:
            v_phase2 = np.array([d2[0]/b2[0]])
        else:
            a2[0] = 0
            c2[-1] = 0
            v_phase2 = tdma_solve(a2, b2, c2, d2)
    else:
        v_phase2 = np.array([])
        
    v_full = np.zeros(N + 1)
    v_full[0] = myu_1
    if len(v_phase1) > 0:
        v_full[1:j] = v_phase1
    v_full[j] = 0.0
    if len(v_phase2) > 0:
        v_full[j+1:N] = v_phase2
    v_full[N] = myu_2

    grad_ice = (v_full[j] - v_full[j-1]) / h 
    grad_water = (v_full[j+1] - v_full[j]) / h
    flux_sum = lambda_1 * grad_ice - lambda_2 * grad_water
    
    if flux_sum <= 1e-9:
        print(f"Остановка j={j}: поток {flux_sum:.4f} слишком мал. Лед не растет.")
        print(f"T_ice(j-1)={v_full[j-1]:.2f}, T_front=0, T_water(j+1)={v_full[j+1]:.2f}")
        break
        
    # Вычисляем шаг по времени tao
    tao = (L_lat * rho_1 * h) / flux_sum
    if tao > 1e10: 
        break
    
    u_new = np.zeros(N + 1)
    u_new[0] = myu_1
    u_new[j] = 0.0 
    
    # Фаза 1 (Лед)
    R1_eff = r1_const / tao
    if n1 > 0:
        a1_y = np.ones(n1)
        b1_y = -(2.0 + R1_eff) * np.ones(n1)
        c1_y = np.ones(n1)
        d1_y = -R1_eff * u[1:j]
        d1_y[0] -= myu_1
        d1_y[-1] -= 0.0 # Граница справа (пока j)
        
        if n1 == 1:
             u_new[1:j] = d1_y[0]/b1_y[0]
        else:
             a1_y[0] = 0; c1_y[-1] = 0
             u_new[1:j] = tdma_solve(a1_y, b1_y, c1_y, d1_y)
             
    # Фаза 2 (Вода)
    R2_eff = r2_const / tao
    if n2 > 0:
        a2_y = np.ones(n2)
        b2_y = -(2.0 + R2_eff) * np.ones(n2)
        c2_y = np.ones(n2)
        d2_y = -R2_eff * u[j+1:N]
        d2_y[0] -= 0.0
        d2_y[-1] -= myu_2
        
        if n2 == 1:
             u_new[j+1:N] = d2_y[0]/b2_y[0]
        else:
             a2_y[0] = 0; c2_y[-1] = 0
             u_new[j+1:N] = tdma_solve(a2_y, b2_y, c2_y, d2_y)
    
    u_new[N] = myu_2



    time += tao
    u = u_new.copy()
    j += 1
    
    time_history.append(time)
    front_history.append(j * h)
    
    if j % 20 == 0:
        print(f"{j:<10} | {time/86400.0:<15.4f} | {tao:<15.4f} | {j*h:<10.4f}")
        results_to_plot.append((x_grid.copy(), u.copy(), time))

# -------------------- ГРАФИКИ СНИЗУ --------------------




#plt.figure(figsize=(10, 6))
#q_ice_list = []
#q_water_list = []
#for x_p, u_p, t_p in results_to_plot:
#    idx_f = np.argmin(np.abs(u_p))
#    q_ice = lambda_1 * (u_p[idx_f] - u_p[idx_f-1]) / h
#    q_water = lambda_2 * (u_p[idx_f+1] - u_p[idx_f]) / h
#    q_ice_list.append(q_ice)
#    q_water_list.append(q_water)
#days_plot = [res[2]/86400 for res in results_to_plot]
#plt.plot(days_plot, q_ice_list, 'blue', label='Поток холода через лед (отводит тепло)')
#plt.plot(days_plot, q_water_list, 'red', label='Поток тепла от воды (греет фронт)')
#plt.title('Баланс тепловых потоков на границе раздела')
#plt.xlabel('Время, сутки')
#plt.ylabel('Тепловой поток, Вт/м²')
#plt.legend()
#plt.grid(True, linestyle=':')
#plt.show()



#plt.figure(figsize=(10, 6))
#indices = np.linspace(0, len(results_to_plot) - 1, 5, dtype=int)
#for idx in indices:
#    x_plot, u_plot, t_plot = results_to_plot[idx]
#    days = t_plot / 86400.0
#    plt.plot(x_plot, u_plot, label=f'День {days:.1f}')
#plt.axhline(0, color='black', lw=1, ls='--')
#plt.xlim(0, 5)
#plt.ylim(myu_1 - 0.5, myu_2 + 0.5)
#plt.title('Профили температуры в различные моменты времени')
#plt.xlabel('Расстояние от поверхности, м')
#plt.ylabel('Температура, °C')
#plt.legend()
#plt.grid(True, which='both', linestyle=':', alpha=0.6)
#plt.show()



#plt.figure(figsize=(12, 5))
#plt.subplot(1, 2, 1)
#t_days = np.array(time_history) / 86400.0
#x_m = np.array(front_history)
#plt.plot(t_days, x_m, 'b-', linewidth=2, label='Ваш расчет')
#plt.title('Движение фронта (обычные оси)')
#plt.xlabel('Время, сутки')
#plt.ylabel('Глубина промерзания, м')
#plt.grid(True)
#plt.tight_layout()
#plt.show()