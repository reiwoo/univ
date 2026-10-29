import pandas as pd
import numpy as np

# 1. Ввод исходных данных
data = {
    'x1': [164, 134, 264, 142, 294, 120, 96, 102, 204, 118, 124, 299, 234, 200, 154, 334, 242, 202, 304, 134, 464, 499, 202, 114, 173, 374, 278, 143, 136, 122, 180, 222, 210, 128, 192, 300],
    'x2': [94, 94, 84, 164, 134, 114, 154, 264, 164, 114, 174, 54, 114, 164, 194, 164, 134, 154, 114, 134, 114, 164, 164, 234, 264, 134, 134, 164, 154, 234, 264, 194, 134, 194, 174, 31],
    'x3': [66, 36, 68, 44, 96, 32, 38, 23, 31, 24, 25, 42, 36, 32, 28, 46, 37, 33, 43, 26, 59, 62, 33, 24, 30, 50, 40, 27, 25, 25, 30, 35, 33, 25, 32, 42],
    'x4': [22, 26, 20, 23, 18, 22, 26, 30, 25, 22, 18, 31, 36, 23, 21, 30, 24, 24, 30, 20, 36, 38, 24, 22, 19, 32, 27, 20, 22, 22, 19, 25, 28, 19, 29, 26]
}

df = pd.DataFrame(data)
n = len(df) # Количество наблюдений (36)

print(f"Количество наблюдений n = {n}\n")

# --- БЛОК РУЧНОГО ВЫЧИСЛЕНИЯ СРЕДНЕГО И СТАНДАРТНОГО ОТКЛОНЕНИЯ ---

# 1. Вычисляем среднее арифметическое (X_bar)
mean_vals = df.mean()

print("--- 1. Средние значения (X_bar) ---")
print(mean_vals)
print("\n")
std_vals = df.std(ddof=0) 

print("--- 2. Среднеквадратические отклонения (Sigma) ---")
print("Вычислено по формуле: sqrt( sum((x - x_bar)^2) / n )")
print(std_vals)
print("\n")
df_std = (df - mean_vals) / std_vals

print("--- 3. Матрица стандартизированных значений Z (первые 5 строк) ---")
print(df_std.head())
print("\n")
corr_matrix = df_std.corr()

print("--- 4. Матрица парных корреляций R ---")
print(corr_matrix)
print("\n")

eigenvalues, eigenvectors = np.linalg.eig(corr_matrix)
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]
U_lecture = eigenvectors / eigenvectors[0, :]

# 5. Собственные числа и нормированные векторы (уже есть в вашем коде)
# eigenvectors здесь — это уже матрица V (нормированные векторы)
V = eigenvectors 

# 6. Расчет матрицы факторного отображения A = V * Lambda^(1/2)
# Используем все 4 компонента
A = V @ np.diag(np.sqrt(eigenvalues))

print("--- 7. Матрица факторного отображения A ---")
# В лекции строки - признаки, столбцы - факторы
print(pd.DataFrame(A, index=['x1', 'x2', 'x3', 'x4'], columns=['F1', 'F2', 'F3', 'F4']))
print("\n")

# 7. Расчет обратной матрицы A^-1
A_inv = np.linalg.inv(A)

print("--- 8. Обратная матрица A^-1 ---")
print(pd.DataFrame(A_inv, index=['F1', 'F2', 'F3', 'F4'], columns=['x1', 'x2', 'x3', 'x4']))
print("\n")

# 8. Расчет матрицы главных компонент F = A^-1 * Z'
# Z_prime - это транспонированная матрица df_std
Z_prime = df_std.values.T
F = A_inv @ Z_prime

# Для удобства выведем транспонированную матрицу F (объекты в строках)
# Создаем DataFrame для удобства
F_df = pd.DataFrame(F.T, columns=['F1', 'F2', 'F3', 'F4'])

# Настройка pandas для отображения всех строк
pd.set_option('display.max_rows', None) 
pd.set_option('display.float_format', '{:.6f}'.format)

print("--- 9. ПОЛНАЯ МАТРИЦА ГЛАВНЫХ КОМПОНЕНТ F ---")
print(F_df)

# Возвращаем настройки обратно (опционально)
pd.reset_option('display.max_rows')