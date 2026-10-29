import numpy as np
import matplotlib.pyplot as plt

l = 5.0          
N = 5000         # Число узлов сетки
h = l / N        # Шаг по пространству
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

# Инициализация поля температуры
u = np.full(N + 1, u_0_val, dtype=float)
u[0] = myu_1

# Вспомогательные коэффициенты r_i (без учета tao, см. обсуждение алгоритма)
# r = (Cp * rho * h^2) / lambda
# Обратите внимание: в уравнении (1) Cp стоит как объемная теплоемкость (rho*c) или удельная?
# Обычно уравнение heat eq: rho*c * dT/dt = div(lambda dT/dx).
# Тогда в разностной схеме r = (rho * c * h^2) / lambda.
r1_const = (c_1 * rho_1 * h**2) / lambda_1
r2_const = (c_2 * rho_2 * h**2) / lambda_2

# -------------------- ФУНКЦИЯ ПРОГОНКИ (TDMA) --------------------
def tdma_solve(a, b, c, d):
    """
    Решает систему Ax = d методом прогонки.
    a - нижняя диагональ, b - главная, c - верхняя.
    """
    n = len(d)
    ac, bc, cc, dc = map(np.array, (a, b, c, d)) # Копии
    for i in range(1, n):
        m = ac[i] / bc[i-1]
        bc[i] = bc[i] - m * cc[i-1]
        dc[i] = dc[i] - m * dc[i-1]
    x = np.zeros(n)
    x[-1] = dc[-1] / bc[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (dc[i] - cc[i] * x[i+1]) / bc[i]
    return x

# -------------------- ОСНОВНОЙ ЦИКЛ ПО ФРОНТУ --------------------
# j - индекс узла, где находится фронт фазового перехода.
# Фронт движется от x[1] до x[N-1]
time = 0.0
time_history = [0.0]
front_history = [0.0] # Фронт стартует из 0 (по условию u(0)=myu_1, u(x)=4, скачок в 0)

# Начинаем с j=1 (первый шаг фронта уже сделан или идет от 0 к 1)
# Для алгоритма "ловля в узел", мы ищем время, чтобы фронт перешел из j в j+1.
# Однако, начальное поле u(x)=4, кроме u(0). Фронт "начинается" между 0 и 1.
# Будем считать, что сейчас фронт находится в узле j, и мы ищем tao для перехода.

u[0] = myu_1
u[1:] = u_0_val

j = 1 # Индекс узла фронта

# Максимальное время (из вашего условия _t=210*84600)
T_max = 210.0 * 86400.0 

results_to_plot = [] # Сохраним пару профилей

print(f"{'Step (j)':<10} | {'Time (days)':<15} | {'Tau (s)':<15} | {'Front (m)':<10}")

while j < N and time < T_max:
    # -----------------------------------------------------------
    # ШАГ 1: ПРЕДИКТОР (Вычисление v_i) - Уравнения (11) и (12)
    # -----------------------------------------------------------
    # Нам нужны v_i, которые НЕ зависят от tao (в явном виде).
    # Уравнение (11): v_{i-1} - (2 + r1)*v_i + v_{i+1} = -r1 * u_old_i
    
    # --- Фаза 1 (Лед): индексы 0 ... j ---
    # Неизвестные v в узлах 1 ... j-1. 
    # v[0] = myu_1, v[j] = 0 (на фронте температура 0)
    
    # Размер системы для Фазы 1: (j-1) уравнений
    n1 = j - 1
    if n1 > 0:
        a1 = np.ones(n1)  # Нижняя диагональ (коэф 1)
        b1 = -(2.0 + r1_const) * np.ones(n1) # Главная
        c1 = np.ones(n1)  # Верхняя
        # Правая часть
        d1 = -r1_const * u[1:j]
        # Граничные условия для v
        # Уравнение для i=1: v_0 - (2+r)v_1 + v_2 = RHS -> -(2+r)v_1 + v_2 = RHS - v_0
        d1[0] -= myu_1  # v_0 = myu_1
        # Уравнение для i=j-1: v_{j-2} - (2+r)v_{j-1} + v_j = RHS -> ... = RHS - v_j
        d1[-1] -= 0.0   # v_j = 0
        
        # Решаем, если есть внутренние узлы (n1 > 0)
        if n1 == 1: # TDMA не работает для 1 элемента, решаем скалярно
             v_phase1 = np.array([d1[0]/b1[0]])
        else:
             # Подправляем диагонали для tdma (первый элемент a и последний c - 0, но функция сама разберется по индексам)
             # Функция tdma ожидает массивы полной длины, a[0] не используется
             a1[0] = 0 
             c1[-1] = 0
             v_phase1 = tdma_solve(a1, b1, c1, d1)
    else:
        v_phase1 = np.array([])

    # --- Фаза 2 (Вода): индексы j ... N ---
    # Неизвестные v в узлах j+1 ... N-1
    # v[j] = 0, v[N] = myu_2
    
    n2 = (N - 1) - (j + 1) + 1 # количество внутренних узлов справа
    # Индексы: j+1, j+2, ..., N-1
    
    if n2 > 0:
        a2 = np.ones(n2)
        b2 = -(2.0 + r2_const) * np.ones(n2)
        c2 = np.ones(n2)
        d2 = -r2_const * u[j+1:N]
        
        # ГУ слева для фазы 2 (v_j = 0)
        d2[0] -= 0.0
        # ГУ справа для фазы 2 (v_N = myu_2)
        d2[-1] -= myu_2
        
        if n2 == 1:
            v_phase2 = np.array([d2[0]/b2[0]])
        else:
            a2[0] = 0
            c2[-1] = 0
            v_phase2 = tdma_solve(a2, b2, c2, d2)
    else:
        v_phase2 = np.array([])
        
    # Собираем полное поле v (для удобства доступа по индексам)
    v_full = np.zeros(N + 1)
    v_full[0] = myu_1
    if len(v_phase1) > 0:
        v_full[1:j] = v_phase1
    v_full[j] = 0.0
    if len(v_phase2) > 0:
        v_full[j+1:N] = v_phase2
    v_full[N] = myu_2

    # -----------------------------------------------------------
    # ШАГ 2: ВЫЧИСЛЕНИЕ TAU (Улучшенный расчет)
    # -----------------------------------------------------------
    # Считаем градиенты (производные) температуры на фронте
    # Поток из льда (отрицательный, так как v[j-1] < 0)
    grad_ice = (v_full[j] - v_full[j-1]) / h 
    
    # Поток из воды (положительный, так как v[j+1] > 0)
    grad_water = (v_full[j+1] - v_full[j]) / h
    
    # Суммарный поток тепла, который идет на фазовый переход (замерзание)
    # По закону Стефана: L*rho*v = lambda1*grad_ice - lambda2*grad_water
    # Скорость v = h/tao
    flux_sum = lambda_1 * grad_ice - lambda_2 * grad_water
    
    # Проверка: если поток отрицательный, значит вода греет сильнее, чем мороз холодит
    if flux_sum <= 1e-9:
        print(f"Остановка j={j}: поток {flux_sum:.4f} слишком мал. Лед не растет.")
        # Для отладки посмотрим, что с температурами рядом с фронтом
        print(f"T_ice(j-1)={v_full[j-1]:.2f}, T_front=0, T_water(j+1)={v_full[j+1]:.2f}")
        break
        
    # Вычисляем шаг по времени tao
    tao = (L_lat * rho_1 * h) / flux_sum
    # Если tao слишком маленькое или огромное, это тоже сигнал об ошибке
    if tao > 1e10: 
        break
    # -----------------------------------------------------------
    # ШАГ 3: КОРРЕКТОР (Вычисление y^j_i, то есть u_new) - Уравнения (7) и (8)
    # -----------------------------------------------------------
    # Теперь tao известно. Решаем обычную неявную схему.
    # (1/tao)*r * (y_new - y_old) = Delta(y_new)
    # => y_{i-1} - (2 + r/tao)y_i + y_{i+1} = -(r/tao)*y_old
    # Здесь "r" из кода выше (r_const) это (Cp*rho*h^2/lambda).
    # Коэффициент в уравнении будет R_eff = r_const / tao.
    
    u_new = np.zeros(N + 1)
    u_new[0] = myu_1
    u_new[j] = 0.0 # В "старой" схеме ловли фронт в узле j (или j+1 в конце шага?)
    # Тонкий момент: на этом шаге по времени фронт перемещается из j в j+1.
    # В момент t + tao фронт будет в j+1. Значит u_new[j+1] должно стать 0.
    # Но уравнения (7) и (8) написаны для текущей конфигурации. 
    # Обычно в этом методе сначала пересчитывают поле T при фиксированном фронте, 
    # а потом сдвигают фронт.
    
    # --- Фаза 1 (Лед) с учетом tao ---
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
             
    # --- Фаза 2 (Вода) с учетом tao ---
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

    # -----------------------------------------------------------
    # ОБНОВЛЕНИЕ
    # -----------------------------------------------------------
    time += tao
    u = u_new.copy()
    
    # Сдвигаем фронт
    j += 1
    # Теперь узел j, который был 0 (фронтом), становится льдом на следующем шаге.
    # А узел j+1 станет новым фронтом (0).
    
    time_history.append(time)
    front_history.append(j * h)
    
    if j % 20 == 0:
        print(f"{j:<10} | {time/86400.0:<15.4f} | {tao:<15.4f} | {j*h:<10.4f}")
        results_to_plot.append((x_grid.copy(), u.copy(), time))

# -------------------- ГРАФИКИ СНИЗУ --------------------


plt.figure(figsize=(10, 6))
q_ice_list = []
q_water_list = []
for x_p, u_p, t_p in results_to_plot:
    idx_f = np.argmin(np.abs(u_p))
    q_ice = lambda_1 * (u_p[idx_f] - u_p[idx_f-1]) / h
    q_water = lambda_2 * (u_p[idx_f+1] - u_p[idx_f]) / h
    
    h_cur = j * h
    if h_cur > 1e-12 and h_cur < l - 1e-12:
        q_ice_anal = lambda_1 * abs(myu_1) / h_cur
        q_water_anal = lambda_2 * myu_2 / (l - h_cur)
    else:
        q_ice_anal = np.nan; q_water_anal = np.nan

    print(f"j={j}, h={h_cur:.3f} m, q_ice={q_ice:.3f}, q_water={q_water:.3f}, q_sum={flux_sum:.3f}")
    print(f"  anal: q_ice={q_ice_anal:.3f}, q_water={q_water_anal:.3f}")
    q_ice_list.append(q_ice)
    q_water_list.append(q_water)
days_plot = [res[2]/86400 for res in results_to_plot]
plt.plot(days_plot, q_ice_list, 'blue', label='Поток холода через лед (отводит тепло)')
plt.plot(days_plot, q_water_list, 'red', label='Поток тепла от воды (греет фронт)')
plt.title('Баланс тепловых потоков на границе раздела')
plt.xlabel('Время, сутки')
plt.ylabel('Тепловой поток, Вт/м²')
plt.legend()
plt.grid(True, linestyle=':')
plt.show()







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