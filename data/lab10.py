import numpy as np
import pandas as pd
i = 14 

data_matrix = np.array([
    [9.3 + 0.1*i, 8.9 + 0.1*i, 6.5 + 0.1*i],
    [9.4 + 0.1*i, 9.1 + 0.1*i, 7.1 + 0.1*i], 
    [12.6 + 0.1*i, 9.8 + 0.1*i, 8.0 + 0.1*i] 
])

print(f"\nМатрица данных (i={i}):")
df = pd.DataFrame(data_matrix, 
                  index=['1001-1500 см³', '1501-2000 см³', 'Более 2000 см³'],
                  columns=['Бензин со свинцом', 'Бензин без свинца', 'Дизельное топливо'])
print(df.round(2).to_string())


n = 4  
np.random.seed(42)

car_data = np.zeros((n, 3, 3))

for car in range(n):
    for vol in range(3):
        for fuel in range(3):
            base = data_matrix[vol, fuel]
            individual_effect = np.random.normal(0, 0.3)
            error = np.random.normal(0, 0.2)
            car_data[car, vol, fuel] = base + individual_effect + error

print(f"\nДанные для {n} автомобилей (первые 2 автомобиля):")
for car in range(min(2, n)):
    print(f"\nАвтомобиль {car+1}:")
    car_df = pd.DataFrame(car_data[car], 
                          index=['1001-1500 см³', '1501-2000 см³', 'Более 2000 см³'],
                          columns=['Бензин со свинцом', 'Бензин без свинца', 'Дизельное топливо'])
    print(car_df.round(2).to_string())

print("\n" + "="*70)
print("РАСЧЕТ ΣT²_AH и ΣT²_BH")
print("="*70)
a = 3  
b = 3  
sums_AH = np.zeros((n, a)) 

for car in range(n):
    for level_a in range(a):
        sum_ah = np.sum(car_data[car, level_a, :])
        sums_AH[car, level_a] = sum_ah

print("\n1. Суммы по сочетаниям автомобиль × объем двигателя (AH):")
ah_df = pd.DataFrame(sums_AH, 
                     index=[f'Автомобиль {c+1}' for c in range(n)],
                     columns=['1001-1500 см³', '1501-2000 см³', 'Более 2000 см³'])
print(ah_df.round(2).to_string())

ΣT2_AH = np.sum(sums_AH**2)
print(f"\nΣT²_AH = сумма квадратов всех значений в таблице выше")
print(f"       = {ΣT2_AH:.2f}")

sums_BH = np.zeros((n, b))

for car in range(n):
    for level_b in range(b):
        sum_bh = np.sum(car_data[car, :, level_b])
        sums_BH[car, level_b] = sum_bh

print("\n2. Суммы по сочетаниям автомобиль × вид топлива (BH):")
bh_df = pd.DataFrame(sums_BH,
                     index=[f'Автомобиль {c+1}' for c in range(n)],
                     columns=['Бензин со свинцом', 'Бензин без свинца', 'Дизельное топливо'])
print(bh_df.round(2).to_string())

ΣT2_BH = np.sum(sums_BH**2)
print(f"\nΣT²_BH = сумма квадратов всех значений в таблице выше")
print(f"       = {ΣT2_BH:.2f}")


print("\n" + "="*70)
print("ВЫЧИСЛЕНИЕ ОСТАЛЬНЫХ СУММ")
print("="*70)

sums_A = car_data.sum(axis=(0, 2))
ΣT2_A = np.sum(sums_A**2)
print(f"1. ΣT²_A = {ΣT2_A:.2f}")
sums_B = car_data.sum(axis=(0, 1)) 
ΣT2_B = np.sum(sums_B**2)
print(f"2. ΣT²_B = {ΣT2_B:.2f}")

sums_AB = car_data.sum(axis=0) 
ΣT2_AB = np.sum(sums_AB**2)
print(f"3. ΣT²_AB = {ΣT2_AB:.2f}")
sums_H = car_data.sum(axis=(1, 2)) 
ΣT2_H = np.sum(sums_H**2)
print(f"4. ΣT²_H = {ΣT2_H:.2f}")

total_sum = car_data.sum()
(Σx2) = total_sum**2
N = n * a * b
C = (Σx2) / N
print(f"5. C = (Σx)²/N = {(Σx2):.2f}/{N} = {C:.2f}")

Σx22 = np.sum(car_data**2)
print(f"6. Σx² = {Σx22:.2f}")

print("\n" + "="*70)
print("РАСЧЕТ СУММ КВАДРАТОВ (SS) - ИСПРАВЛЕННЫЙ")
print("="*70)

df_A = a - 1  
df_B = b - 1  
df_H = n - 1  
df_AB = (a - 1) * (b - 1)  
df_AH = (a - 1) * (n - 1)  
df_BH = (b - 1) * (n - 1)  
df_ABH = (a - 1) * (b - 1) * (n - 1)  
df_total = N - 1 

print("Степени свободы:")
print(f"  df_A={df_A}, df_B={df_B}, df_H={df_H}")
print(f"  df_AB={df_AB}, df_AH={df_AH}, df_BH={df_BH}")
print(f"  df_ABH={df_ABH}, df_total={df_total}")

SSA = ΣT2_A / (n * b) - C
SSB = ΣT2_B / (n * a) - C
SSH = ΣT2_H / (a * b) - C
SSAB = ΣT2_AB / n - C - SSA - SSB
SSAH = ΣT2_AH / b - C - SSA - SSH
SSBH = ΣT2_BH / a - C - SSB - SSH

SS_total = Σx22 - C
SSABH = SS_total - SSA - SSB - SSH - SSAB - SSAH - SSBH
print(f"\nСуммы квадратов (SS):")
print(f"  SSA = ΣT²_A/(n*b) - C = {ΣT2_A:.2f}/({n}*{b}) - {C:.2f} = {SSA:.4f}")
print(f"  SSB = ΣT²_B/(n*a) - C = {ΣT2_B:.2f}/({n}*{a}) - {C:.2f} = {SSB:.4f}")
print(f"  SSH = ΣT²_H/(a*b) - C = {ΣT2_H:.2f}/({a}*{b}) - {C:.2f} = {SSH:.4f}")
print(f"  SSAB = ΣT²_AB/n - C - SSA - SSB = {SSAB:.4f}")
print(f"  SSAH = ΣT²_AH/b - C - SSA - SSH = {ΣT2_AH:.2f}/{b} - {C:.2f} - {SSA:.2f} - {SSH:.2f} = {SSAH:.4f}")
print(f"  SSBH = ΣT²_BH/a - C - SSB - SSH = {ΣT2_BH:.2f}/{a} - {C:.2f} - {SSB:.2f} - {SSH:.2f} = {SSBH:.4f}")
print(f"  SSABH = остаток = {SSABH:.4f}")
print(f"  SS_total = Σx² - C = {SS_total:.4f}")


print("\n" + "="*70)
print("ПРОВЕРКА РАСЧЕТОВ")
print("="*70)

SS_sum = SSA + SSB + SSH + SSAB + SSAH + SSBH + SSABH
diff = abs(SS_total - SS_sum)
print(f"1. Сумма всех SS = {SS_sum:.6f}")
print(f"   SS_total = {SS_total:.6f}")
print(f"   Разница = {diff:.10f}")
if diff < 0.0001:
    print("   ✓ Проверка пройдена!")
else:
    print("   ✗ Ошибка в расчетах!")

print(f"\n2. Альтернативный расчет:")
SS_A_by_car = 0
for car in range(n):
    car_sum = np.sum(sums_AH[car, :])
    SS_A_car = np.sum((sums_AH[car, :] - car_sum/(a))**2) / b
    SS_A_by_car += SS_A_car

print(f"   SS_A_by_car = {SS_A_by_car:.4f}")
print(f"   SSAH = {SSAH:.4f}")


print("\n" + "="*70)
print("РАСЧЕТ СРЕДНИХ КВАДРАТОВ И F-КРИТЕРИЕВ")
print("="*70)
MSA = SSA / df_A if df_A > 0 else 0
MSB = SSB / df_B if df_B > 0 else 0
MSH = SSH / df_H if df_H > 0 else 0
MSAB = SSAB / df_AB if df_AB > 0 else 0
MSAH = SSAH / df_AH if df_AH > 0 else 0
MSBH = SSBH / df_BH if df_BH > 0 else 0
MSABH = SSABH / df_ABH if df_ABH > 0 else 0

print("Средние квадраты (MS):")
print(f"  MSA = {MSA:.4f}, MSB = {MSB:.4f}, MSH = {MSH:.4f}")
print(f"  MSAB = {MSAB:.4f}, MSAH = {MSAH:.4f}, MSBH = {MSBH:.4f}")
print(f"  MSABH = {MSABH:.4f}")

FA = MSA / MSAH if MSAH > 0 else 0
FB = MSB / MSBH if MSBH > 0 else 0
FH = MSH / MSABH if MSABH > 0 else 0
FAB = MSAB / MSABH if MSABH > 0 else 0

print(f"\nF-критерии:")
print(f"  FA = MSA/MSAH = {MSA:.4f}/{MSAH:.4f} = {FA:.4f}")
print(f"  FB = MSB/MSBH = {MSB:.4f}/{MSBH:.4f} = {FB:.4f}")
print(f"  FH = MSH/MSABH = {MSH:.4f}/{MSABH:.4f} = {FH:.4f}")
print(f"  FAB = MSAB/MSABH = {MSAB:.4f}/{MSABH:.4f} = {FAB:.4f}")

print("\n" + "="*70)
print("ДЕТАЛЬНЫЙ РАСЧЕТ ΣT²_AH и ΣT²_BH")
print("="*70)

print("Для наглядности вычислим ΣT²_AH пошагово:")

print("\nТаблица AH (суммы по видам топлива для каждого автомобиля и объема):")
ah_table = []

for car in range(n):
    car_row = []
    for vol in range(a):
        sum_val = np.sum(car_data[car, vol, :])
        ah_table.append((car, vol, sum_val))
        car_row.append(sum_val)
        print(f"  Автомобиль {car+1}, Объем {vol+1}: {sum_val:.2f}")
    
    row_str = ", ".join(f"{x:.2f}" for x in car_row)
    print(f"  Автомобиль {car+1}: [{row_str}]")

print(f"\nВсего значений: {len(ah_table)}")

squares_AH = [val**2 for _, _, val in ah_table]
ΣT2_AH_calc = sum(squares_AH)
print(f"\nКвадраты значений:")
for i, (car, vol, val) in enumerate(ah_table):
    print(f"  ({car+1},{vol+1}): {val:.2f}² = {val**2:.2f}")

print(f"\nΣT²_AH = сумма квадратов = {sum(squares_AH):.2f}")
print(f"Проверка: ранее вычислено {ΣT2_AH:.2f}")

print("\n" + "-"*70)
print("Таблица BH (суммы по объемам двигателя для каждого автомобиля и вида топлива):")
bh_table = []

for car in range(n):
    car_row = []
    for fuel in range(b):
        sum_val = np.sum(car_data[car, :, fuel])
        bh_table.append((car, fuel, sum_val))
        car_row.append(sum_val)
    
    fuel_names = ['Бенз.св', 'Бенз.б/с', 'Дизель']
    row_str = ", ".join(f"{fuel_names[f]}: {car_row[f]:.2f}" for f in range(b))
    print(f"  Автомобиль {car+1}: {row_str}")

squares_BH = [val**2 for _, _, val in bh_table]
ΣT2_BH_calc = sum(squares_BH)
print(f"\nΣT²_BH = сумма квадратов = {ΣT2_BH_calc:.2f}")
print(f"Проверка: ранее вычислено {ΣT2_BH:.2f}")


print("\n" + "="*80)
print("ТАБЛИЦА ДИСПЕРСИОННОГО АНАЛИЗА (ANOVA)")
print("="*80)
print(f"{'Источник вариации':<25} {'SS':<12} {'df':<6} {'MS':<12} {'F':<12}")
print("-"*80)
print(f"{'A (объем двигателя)':<25} {SSA:<12.4f} {df_A:<6} {MSA:<12.4f} {FA:<12.4f}")
print(f"{'B (вид топлива)':<25} {SSB:<12.4f} {df_B:<6} {MSB:<12.4f} {FB:<12.4f}")
print(f"{'H (автомобили)':<25} {SSH:<12.4f} {df_H:<6} {MSH:<12.4f} {FH:<12.4f}")
print(f"{'A×B':<25} {SSAB:<12.4f} {df_AB:<6} {MSAB:<12.4f} {FAB:<12.4f}")
print(f"{'A×H (ошибка A)':<25} {SSAH:<12.4f} {df_AH:<6} {MSAH:<12.4f}")
print(f"{'B×H (ошибка B)':<25} {SSBH:<12.4f} {df_BH:<6} {MSBH:<12.4f}")
print(f"{'A×B×H (остаток)':<25} {SSABH:<12.4f} {df_ABH:<6} {MSABH:<12.4f}")
print(f"{'Общее':<25} {SS_total:<12.4f} {df_total:<6}")
print("="*80)



print("\n" + "="*70)
print("СТАТИСТИЧЕСКИЕ ВЫВОДЫ")
print("="*70)


F_crit_A = 5.14  # df1=2, df2=6
F_crit_B = 5.14  # df1=2, df2=6  
F_crit_H = 3.49  # df1=3, df2=12
F_crit_AB = 3.26  # df1=4, df2=12

print(f"Критические значения F (α=0.05):")
print(f"  Для FA: Fкрит({df_A},{df_AH}) = {F_crit_A:.2f}")
print(f"  Для FB: Fкрит({df_B},{df_BH}) = {F_crit_B:.2f}")
print(f"  Для FH: Fкрит({df_H},{df_ABH}) = {F_crit_H:.2f}")
print(f"  Для FAB: Fкрит({df_AB},{df_ABH}) = {F_crit_AB:.2f}")
print(f"\nВыводы:")
print(f"1. Фактор A (объем): FA = {FA:.2f} {'>' if FA > F_crit_A else '<'} {F_crit_A:.2f} → {'ЗНАЧИМ' if FA > F_crit_A else 'НЕ ЗНАЧИМ'}")
print(f"2. Фактор B (топливо): FB = {FB:.2f} {'>' if FB > F_crit_B else '<'} {F_crit_B:.2f} → {'ЗНАЧИМ' if FB > F_crit_B else 'НЕ ЗНАЧИМ'}")
print(f"3. Индив. различия: FH = {FH:.2f} {'>' if FH > F_crit_H else '<'} {F_crit_H:.2f} → {'ЗНАЧИМ' if FH > F_crit_H else 'НЕ ЗНАЧИМ'}")
print(f"4. Взаимодействие: FAB = {FAB:.2f} {'>' if FAB > F_crit_AB else '<'} {F_crit_AB:.2f} → {'ЗНАЧИМ' if FAB > F_crit_AB else 'НЕ ЗНАЧИМ'}")