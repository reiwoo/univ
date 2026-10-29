import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

districts = list(range(1, 37))

x = [
    164, 134, 264, 142, 294, 120, 96, 102, 204, 118,
    124, 299, 234, 200, 154, 334, 242, 202, 304, 134,
    464, 499, 202, 114, 173, 374, 278, 143, 136, 122,
    180, 222, 210, 128, 192, 300
]

y = [
    66, 36, 68, 44, 96, 32, 38, 23, 31, 24,
    25, 42, 36, 32, 28, 46, 37, 33, 43, 26,
    59, 62, 33, 24, 30, 50, 40, 27, 25, 25,
    30, 35, 33, 25, 32, 42
]

z = [
    22, 26, 20, 23, 18, 22, 26, 30, 25, 22,
    18, 31, 36, 23, 21, 30, 24, 24, 30, 20,
    36, 38, 24, 22, 19, 32, 27, 20, 22, 22,
    19, 25, 28, 19, 29, 26
]

# Начальные центры (из п.2)
xmin = min(x)
xmax = max(x)
xsr = sum(x) / len(x) 

ymin = min(y)
ymax = max(y)
ysr = sum(y) / len(y)

zmin = min(z)
zmax = max(z)
zsr = sum(z) / len(z)

print("НАЧАЛЬНЫЕ ЦЕНТРЫ КЛАСТЕРОВ:")
print(f"Центр 1 (высокий): xmax={xmax}, ymax={ymax}, zmax={zmax}")
print(f"Центр 2 (средний): xsr={xsr:.2f}, ysr={ysr:.2f}, zsr={zsr:.2f}")
print(f"Центр 3 (низкий):  xmin={xmin}, ymin={ymin}, zmin={zmin}")
print()

# Итерационный процесс
iteration = 1
max_iterations = 20  # на всякий случай ограничим

while True:
    print(f"\n{'='*70}")
    print(f"ИТЕРАЦИЯ {iteration}:")
    print('='*70)
    
    # 3. Рассчитываем расстояния до центров
    r1 = [math.sqrt((i - xmax)**2 + (j - ymax)**2 + (k - zmax)**2) for i, j, k in zip(x, y, z)]
    r2 = [math.sqrt((i - xsr)**2 + (j - ysr)**2 + (k - zsr)**2) for i, j, k in zip(x, y, z)]
    r3 = [math.sqrt((i - xmin)**2 + (j - ymin)**2 + (k - zmin)**2) for i, j, k in zip(x, y, z)]
    
    # 4. Определяем кластеры
    clusters = []
    for i in range(len(districts)):
        distances = [r1[i], r2[i], r3[i]]
        min_dist = min(distances)
        
        if distances[0] == min_dist:
            cluster = 1
        elif distances[1] == min_dist:
            cluster = 2
        else:
            cluster = 3
        clusters.append(cluster)
    
    # Статистика по кластерам
    print(f"\nРаспределение по кластерам:")
    for cluster_num in [1, 2, 3]:
        count = clusters.count(cluster_num)
        level = "высокий" if cluster_num == 1 else "средний" if cluster_num == 2 else "низкий"
        district_list = [districts[i] for i in range(len(districts)) if clusters[i] == cluster_num]
        print(f"  Кластер {cluster_num} ({level}): {count} районов - {district_list}")
    
    # 5. Рассчитываем новые центры кластеров
    # Для кластера 1 (высокий) - средние значения точек в этом кластере
    x_cluster1 = [x[i] for i in range(len(x)) if clusters[i] == 1]
    y_cluster1 = [y[i] for i in range(len(y)) if clusters[i] == 1]
    z_cluster1 = [z[i] for i in range(len(z)) if clusters[i] == 1]
    
    xmax2 = sum(x_cluster1) / len(x_cluster1) if x_cluster1 else xmax
    ymax2 = sum(y_cluster1) / len(y_cluster1) if y_cluster1 else ymax
    zmax2 = sum(z_cluster1) / len(z_cluster1) if z_cluster1 else zmax
    
    # Для кластера 2 (средний)
    x_cluster2 = [x[i] for i in range(len(x)) if clusters[i] == 2]
    y_cluster2 = [y[i] for i in range(len(y)) if clusters[i] == 2]
    z_cluster2 = [z[i] for i in range(len(z)) if clusters[i] == 2]
    
    xsr2 = sum(x_cluster2) / len(x_cluster2) if x_cluster2 else xsr
    ysr2 = sum(y_cluster2) / len(y_cluster2) if y_cluster2 else ysr
    zsr2 = sum(z_cluster2) / len(z_cluster2) if z_cluster2 else zsr
    
    # Для кластера 3 (низкий)
    x_cluster3 = [x[i] for i in range(len(x)) if clusters[i] == 3]
    y_cluster3 = [y[i] for i in range(len(y)) if clusters[i] == 3]
    z_cluster3 = [z[i] for i in range(len(z)) if clusters[i] == 3]
    
    xmin2 = sum(x_cluster3) / len(x_cluster3) if x_cluster3 else xmin
    ymin2 = sum(y_cluster3) / len(y_cluster3) if y_cluster3 else ymin
    zmin2 = sum(z_cluster3) / len(z_cluster3) if z_cluster3 else zmin
    
    print(f"\nНОВЫЕ ЦЕНТРЫ КЛАСТЕРОВ:")
    print(f"  Центр 1 (высокий): xmax2={xmax2:.2f}, ymax2={ymax2:.2f}, zmax2={zmax2:.2f}")
    print(f"  Центр 2 (средний): xsr2={xsr2:.2f}, ysr2={ysr2:.2f}, zsr2={zsr2:.2f}")
    print(f"  Центр 3 (низкий):  xmin2={xmin2:.2f}, ymin2={ymin2:.2f}, zmin2={zmin2:.2f}")
    
    # Проверяем сходимость
    centers_changed = False
    tolerance = 0.01  # точность сравнения
    
    if (abs(xmax - xmax2) > tolerance or abs(ymax - ymax2) > tolerance or abs(zmax - zmax2) > tolerance or
        abs(xsr - xsr2) > tolerance or abs(ysr - ysr2) > tolerance or abs(zsr - zsr2) > tolerance or
        abs(xmin - xmin2) > tolerance or abs(ymin - ymin2) > tolerance or abs(zmin - zmin2) > tolerance):
        centers_changed = True
    
    if not centers_changed or iteration >= max_iterations:
        print(f"\n{'='*70}")
        print("ВЫЧИСЛЕНИЯ ЗАВЕРШЕНЫ!")
        print('='*70)
        if iteration >= max_iterations:
            print(f"Достигнуто максимальное число итераций ({max_iterations})")
        else:
            print("Центры кластеров стабилизировались")
        
        print(f"\nФИНАЛЬНАЯ ГРУППИРОВКА РАЙОНОВ (после {iteration} итераций):")
        print("-" * 50)
        
        # Детальная таблица
        print("\nРайон | Такси | Микроавт. | Автобусы | Кластер | Уровень развития")
        print("-" * 70)
        for i in range(len(districts)):
            level = "Высокий" if clusters[i] == 1 else "Средний" if clusters[i] == 2 else "Низкий"
            print(f"{districts[i]:5} | {x[i]:5} | {y[i]:8} | {z[i]:8} | {clusters[i]:7} | {level}")
        
        print(f"\nФИНАЛЬНЫЕ ЦЕНТРЫ КЛАСТЕРОВ:")
        print(f"  Центр 1 (высокий): ({xmax2:.2f}, {ymax2:.2f}, {zmax2:.2f})")
        print(f"  Центр 2 (средний): ({xsr2:.2f}, {ysr2:.2f}, {zsr2:.2f})")
        print(f"  Центр 3 (низкий):  ({xmin2:.2f}, {ymin2:.2f}, {zmin2:.2f})")
        break
    
    # Обновляем центры для следующей итерации
    xmin, ymin, zmin = xmin2, ymin2, zmin2
    xsr, ysr, zsr = xsr2, ysr2, zsr2
    xmax, ymax, zmax = xmax2, ymax2, zmax2
    
    iteration += 1
    
print("\n1. Вектор номеров кластеров (список):")
print("   clusters =", clusters)


# Data from your script
x = [164, 134, 264, 142, 294, 120, 96, 102, 204, 118, 124, 299, 234, 200, 154, 334, 242, 202, 304, 134, 464, 499, 202, 114, 173, 374, 278, 143, 136, 122, 180, 222, 210, 128, 192, 300]
y = [66, 36, 68, 44, 96, 32, 38, 23, 31, 24, 25, 42, 36, 32, 28, 46, 37, 33, 43, 26, 59, 62, 33, 24, 30, 50, 40, 27, 25, 25, 30, 35, 33, 25, 32, 42]
z = [22, 26, 20, 23, 18, 22, 26, 30, 25, 22, 18, 31, 36, 23, 21, 30, 24, 24, 30, 20, 36, 38, 24, 22, 19, 32, 27, 20, 22, 22, 19, 25, 28, 19, 29, 26]

# Final clusters from your output
clusters = [3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 2, 2, 2, 3, 2, 2, 2, 2, 3, 1, 1, 2, 3, 3, 1, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2]

# Colors for the clusters (1=Red, 2=Green, 3=Blue)
colors = {1: 'red', 2: 'green', 3: 'blue'}
point_colors = [colors[c] for c in clusters]

# Create 3D Plot 
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(x, y, z, c=point_colors, s=60, alpha=0.8)

# Labels
ax.set_xlabel('Taxis (X)')
ax.set_ylabel('Minibuses (Y)')
ax.set_zlabel('Buses (Z)')
ax.set_title('K-Means Clustering of Transport Districts')

# Custom Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Cluster 1 (High)', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Cluster 2 (Medium)', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Cluster 3 (Low)', markerfacecolor='blue', markersize=10)
]
ax.legend(handles=legend_elements)

plt.show()