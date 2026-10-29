import numpy as np
import pandas as pd
import scipy.stats as stats

raw_data = [
    [84.3, 79.8, 86.6, 84.8, 81.6, 79.2], 
    [91.0, 93.8, 89.3, 88.1, 93.1, 94.9], 
    [97.0, 99.6, 96.2, 94.6, 98.5, 98.0], 
    [68.0, 64.3, 66.5, 69.6, 70.5, 68.6], 
    [74.7, 75.3, 71.5, 78.2, 76.6, 78.5], 
    [77.0, 80.6, 76.7, 76.2, 80.4, 77.7], 
    [79.5, 81.6, 80.8, 84.5, 84.3, 80.5], 
    [91.1, 95.9, 86.5, 88.6, 89.8, 95.1], 
    [98.5, 96.6, 95.5, 99.4, 93.8, 93.3]  
]

data = np.array(raw_data).reshape(3, 3, 6)

a = 3  
b = 3 
n = 6 
N = a * b * n # 54

sum_total = np.sum(data)
sum_sq_total = np.sum(data**2)

# Суммы по факторам
sum_A = np.sum(data, axis=(1, 2))   # Суммы по Сортам
sum_B = np.sum(data, axis=(0, 2))   # Суммы по Регуляторам
sum_AB = np.sum(data, axis=2)       # Суммы по ячейкам (Взаимодействие)

# Поправочный член
CT = (sum_total ** 2) / N

# 2. Суммы квадратов (SS)
SS_total = sum_sq_total - CT
SS_A = np.sum(sum_A**2) / (b * n) - CT
SS_B = np.sum(sum_B**2) / (a * n) - CT
SS_cells = np.sum(sum_AB**2) / n - CT
SS_AB = SS_cells - SS_A - SS_B
SS_error = SS_total - SS_cells
print(SS_error)

# 3. Степени свободы (df)
df_A = a - 1
df_B = b - 1
df_AB = (a - 1) * (b - 1)
df_error = a * b * (n - 1)

# 4. Средние квадраты (MS)
MS_A = SS_A / df_A
MS_B = SS_B / df_B
MS_AB = SS_AB / df_AB
MS_error = SS_error / df_error

# 5. F-критерий
F_A = MS_A / MS_error
F_B = MS_B / MS_error
F_AB = MS_AB / MS_error
# 6. Критические значения (alpha=0.05)
F_crit_A = stats.f.ppf(0.95, df_A, df_error)
F_crit_B = stats.f.ppf(0.95, df_B, df_error)
F_crit_AB = stats.f.ppf(0.95, df_AB, df_error)
print(F_crit_A, F_crit_B, F_crit_AB)
# Вывод
print(f"{'Источник':<20} | {'SS':<10} | {'df':<3} | {'MS':<10} | {'F_fact':<8} | {'F_table':<8}")
print("-" * 75)
print(f"{'Фактор А (Сорт)':<20} | {SS_A:<10.2f} | {df_A:<3} | {MS_A:<10.2f} | {F_A:<8.2f} | {F_crit_A:<8.2f}")
print(f"{'Фактор В (Рег)':<20} | {SS_B:<10.2f} | {df_B:<3} | {MS_B:<10.2f} | {F_B:<8.2f} | {F_crit_B:<8.2f}")
print(f"{'Взаимодействие AB':<20} | {SS_AB:<10.2f} | {df_AB:<3} | {MS_AB:<10.2f} | {F_AB:<8.2f} | {F_crit_AB:<8.2f}")
print(f"{'Ошибка':<20} | {SS_error:<10.2f} | {df_error:<3} | {MS_error:<10.2f} | {'-':<8} | {'-':<8}")
print(f"{'Всего':<20} | {SS_total:<10.2f} | {N-1:<3} | {'-':<10} | {'-':<8} | {'-':<8}")