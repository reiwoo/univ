import numpy as np

# 1. Исходная матрица парных корреляций R
R = np.array([
    [1.000000, -0.364422,  0.628374,  0.674808],
    [-0.364422, 1.000000, -0.431235, -0.271130],
    [0.628374, -0.431235,  1.000000,  0.195700],
    [0.674808, -0.271130,  0.195700,  1.000000]
])

# 2. Ваши собственные числа (Lambda)
lambdas = [2.3119409, 0.88286459, 0.64019081, 0.1650037]

# Списки для хранения векторов
U_list = []
V_list = []
norms = []

print("--- Расчет по методике лекции ---")

for j, lam in enumerate(lambdas):
    # Формируем матрицу (R - lambda*E)
    A_full = R - np.eye(4) * lam
    
    # Решаем систему (15), полагая u1 = 1
    # Берем подматрицу 3x3 (последние 3 строки и столбца)
    A_sub = A_full[1:, 1:]
    # Свободные члены - первый столбец последних 3 строк (с минусом)
    B_sub = -A_full[1:, 0]
    
    # Находим компоненты u2, u3, u4
    u_rest = np.linalg.solve(A_sub, B_sub)
    u_vec = np.array([1.0, u_rest[0], u_rest[1], u_rest[2]])
    U_list.append(u_vec)
    
    # Вычисляем норму вектора по формуле (13)
    norm_u = np.sqrt(np.sum(u_vec**2))
    norms.append(norm_u)
    
    # Получаем нормированный вектор Vj
    v_vec = u_vec / norm_u
    V_list.append(v_vec)

# Преобразуем в матрицы для красивого вывода (столбцы - векторы)
U_matrix = np.array(U_list).T
V_matrix = np.array(V_list).T

print("\n1. Матрица ненормированных векторов U (u1 = 1):")
print(U_matrix)

print("\n2. Нормы векторов |Uj|:")
for j, n in enumerate(norms):
    print(f"|U{j+1}| = {n:.6f}")

print("\n3. Итоговая матрица нормированных векторов V (как в Numpy):")
print(V_matrix)