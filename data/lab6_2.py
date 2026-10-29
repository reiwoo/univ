import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

y = np.array([34, 55, 64, 76, 84, 94, 99, 102, 110, 116, 120, 126, 136, 140, 152, 166])
t = np.arange(1, len(y) + 1)
n = len(y)

b, a = np.polyfit(t, y, 1)
y_pred = a + b * t
residuals = y - y_pred
print(y_pred)
print(residuals)
print(f"--- 1. Уравнение тренда ---")
print(f"y = {a:.4f} + {b:.4f} * t\n")

print(f"--- 2. Анализ остатков ---")
mean_e = np.mean(residuals)
std_e = np.std(residuals, ddof=1)
t_calc = (abs(mean_e) / std_e) * np.sqrt(n)
t_crit = stats.t.ppf(1 - 0.05/2, n - 1)
print(f"а) M[e] = 0: t_calc = {t_calc:.10f}, t_crit = {t_crit:.4f}")
print("   Гипотеза принимается" if t_calc < t_crit else "   Гипотеза отклоняется")

p = 0
for i in range(1, n - 1):
    if (residuals[i] > residuals[i-1] and residuals[i] > residuals[i+1]) or \
       (residuals[i] < residuals[i-1] and residuals[i] < residuals[i+1]):
        p += 1
p_crit = int(2/3 * (n - 2) - 1.96 * np.sqrt((16*n - 29)/90))
print(f"б) Поворотные точки: p = {p}, p_crit = {p_crit}")
print("   Ряд случайный" if p > p_crit else "   Ряд неслучайный")

# в) Критерий Дарбина-Уотсона (автокорреляция)
diff_e = np.diff(residuals)
dw = np.sum(diff_e**2) / np.sum(residuals**2)
print(f"в) Дарбин-Уотсон: DW = {dw:.4f} (норма около 2)")
# Табличные значения для n=12, k=1: dL=1.08, dU=1.36
if 1.36 < dw < 2.64:
    print("   Автокорреляция отсутствует")
else:
    print("   Есть подозрение на автокорреляцию")

# г) Нормальный закон (RS-критерий)
d1, d2 = 3.0, 4.2 
rs = (np.max(residuals) - np.min(residuals)) / std_e

print(f"г) RS-критерий: RS = {rs:.4f}")
if d1 <= rs <= d2:
    print(f"   Результат: {rs:.4f} попадает в интервал [{d1}, {d2}]. Соответствует норме.")
else:
    print(f"   Результат: {rs:.4f} ВНЕ интервала [{d1}, {d2}]. НЕ соответствует норме.")
as_val = skew(residuals)      # Асимметрия
ex_val = kurtosis(residuals)  # Эксцесс (уже за вычетом 3)

# Ошибки (приблизительные формулы для оценки)
sigma_as = np.sqrt(6 / n)
sigma_ex = np.sqrt(24 / n)

print(f"--- Дополнительный анализ формы распределения ---")
print(f"Асимметрия (As) = {as_val:.4f} (норма: |As| < {3*sigma_as:.2f})")
print(f"Эксцесс (Ex) = {ex_val:.4f} (норма: |Ex| < {3*sigma_ex:.2f})")

if abs(as_val) < 3*sigma_as and abs(ex_val) < 3*sigma_ex:
    print("Вывод: Распределение остатков близко к нормальному.")
else:
    print("Вывод: Есть значительные отклонения от нормального распределения.")


# 3. Средняя относительная ошибка (MAPE)
mape = np.mean(np.abs(residuals / y)) * 100
print(f"\n--- 3. Точность ---")
print(f"MAPE = {mape:.2f}%")

# 4. Прогноз на IV кв 2024 (t = 20)
t_future = 22
y_future_point = a + b * t_future

# Интервальный прогноз
# Se (стандартная ошибка регрессии)
se = np.sqrt(np.sum(residuals**2) / (n - 2))
t_stud = stats.t.ppf(1 - 0.05/2, n - 2)
sum_t_sq = np.sum((t - np.mean(t))**2)

# Величина U(k) по формуле из лекции
uk = se * t_stud * np.sqrt(1 + 1/n + (t_future - np.mean(t))**2 / sum_t_sq)

print(f"\n--- 4. Прогноз на IV кв 2024 (t={t_future}) ---")
print(f"Точечный прогноз: {y_future_point:.3f}")
print(f"Доверительный интервал: [{y_future_point - uk:.3f} ; {y_future_point + uk:.3f}]")

# Визуализация
plt.figure(figsize=(10, 5))
plt.plot(t, y, 'ob', label='Факт')
plt.plot(t, y_pred, '-r', label='Тренд')
plt.scatter(t_future, y_future_point, color='green', marker='x', s=100, label='Прогноз')
plt.errorbar(t_future, y_future_point, yerr=uk, fmt='none', ecolor='green', capsize=5, label='Интервал')
plt.title('Прогноз ВВП (Линейная модель)')
plt.xlabel('Кварталы (начиная с 2020)')
plt.ylabel('ВВП')
plt.legend()
plt.grid(True)
plt.show()