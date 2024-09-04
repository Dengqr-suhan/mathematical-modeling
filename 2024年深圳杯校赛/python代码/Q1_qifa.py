import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 震动波传播速度 (m/s)
v = 340

# 监测设备的数据：经度(°), 纬度(°), 高程(m), 音爆到达时间(s)
data = np.array([
    [110.241, 27.204, 824, 100.767],
    [110.780, 27.456, 727, 112.220],
    [110.712, 27.785, 742, 188.020],
    [110.251, 27.825, 850, 258.985],
    [110.524, 27.617, 786, 118.443],
    [110.467, 27.921, 678, 266.871],
    [110.047, 27.121, 575, 163.024]
])

# 经纬度转换为距离
def lon_lat_to_distance(lon1, lat1, lon2, lat2):
    dx = (lon2 - lon1) * 97.304 * 1000  # 经度差异 -> 米
    dy = (lat2 - lat1) * 111.263 * 1000  # 纬度差异 -> 米
    return dx, dy

# 目标函数: 误差平方和
def objective_function(vars, selected_data):
    x0, y0, z0, t0 = vars
    error_sum = 0
    for i in range(selected_data.shape[0]):
        lon_i, lat_i, z_i, t_i = selected_data[i]
        dx, dy = lon_lat_to_distance(lon_i, lat_i, x0, y0)
        dz = z_i - z0
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        t_pred = t0 + distance / v
        error_sum += (t_pred - t_i) ** 2
    return error_sum

# 遗传算法实现
def genetic_algorithm(selected_data, population_size=100, generations=500, mutation_rate=0.01, bounds=None):
    if bounds is None:
        bounds = [(110.0, 111.0), (27.0, 28.0), (500, 1000), (0, 300)]
    
    # 初始化种群
    population = np.random.rand(population_size, len(bounds))
    for i in range(len(bounds)):
        population[:, i] = population[:, i] * (bounds[i][1] - bounds[i][0]) + bounds[i][0]
    
    best_solution = None
    best_error = float('inf')
    error_history = []
    
    for generation in range(generations):
        # 评估种群
        fitness = np.array([objective_function(ind, selected_data) for ind in population])
        
        # 选择最优个体
        if np.min(fitness) < best_error:
            best_error = np.min(fitness)
            best_solution = population[np.argmin(fitness)]
        
        # 记录当前最优误差
        error_history.append(best_error)
        print(f"Generation {generation+1}, Best Error: {best_error:.6f}")
        
        # 选择 (轮盘赌选择法)
        fitness = 1 / (1 + fitness)  # 转换为适应度值
        probabilities = fitness / np.sum(fitness)
        selected_indices = np.random.choice(np.arange(population_size), size=population_size, p=probabilities)
        selected_population = population[selected_indices]
        
        # 交叉 (单点交叉)
        offspring = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected_population[i], selected_population[i+1]
            crossover_point = np.random.randint(1, len(bounds)-1)
            child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
            offspring.append(child1)
            offspring.append(child2)
        
        offspring = np.array(offspring)
        
        # 变异
        for i in range(offspring.shape[0]):
            if np.random.rand() < mutation_rate:
                mutation_point = np.random.randint(len(bounds))
                offspring[i, mutation_point] = np.random.rand() * (bounds[mutation_point][1] - bounds[mutation_point][0]) + bounds[mutation_point][0]
        
        # 更新种群
        population = offspring
    
    return best_solution, error_history

# 使用随机选择和遗传算法求解
best_solution = None
best_error = float('inf')
best_error_history = []
best_selected_indices = None
num_trials = 100  # 尝试次数

for _ in range(num_trials):
    # 随机选择4个不同的监测设备数据
    indices = np.random.choice(data.shape[0], 4, replace=False)
    selected_data = data[indices]
    
    # 执行遗传算法
    solution, error_history = genetic_algorithm(selected_data)
    
    # 计算当前解的误差
    current_error = objective_function(solution, selected_data)
    if current_error < best_error:
        best_error = current_error
        best_solution = solution
        best_error_history = error_history
        best_selected_indices = indices

# 输出最佳结果
x0, y0, z0, t0 = best_solution
selected_devices = data[best_selected_indices]
device_numbers = best_selected_indices + 1  # 设备编号从1开始计数
print(f"\n选择的四个设备编号为: {device_numbers.tolist()}")
print(f"\n音爆发生位置经度: {x0:.6f}°")
print(f"音爆发生位置纬度: {y0:.6f}°")
print(f"音爆发生位置高程: {z0:.2f}米")
print(f"音爆发生时间: {t0:.3f}秒")

# 绘制适应度随代数变化的曲线
plt.figure(figsize=(10, 6))
plt.plot(best_error_history, label='Best Error')
plt.xlabel('Generation')
plt.ylabel('Error')
plt.title('Error Convergence Over Generations')
plt.legend()
plt.show()

# 三维可视化最终解的设备位置及预测音爆源位置
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制选定设备的位置
for i in range(len(selected_devices)):
    ax.scatter(selected_devices[i, 0] * 97304, selected_devices[i, 1] * 111263, selected_devices[i, 2], s=100, label=f'Device {device_numbers[i]}')

# 绘制音爆源的位置
ax.scatter(x0 * 97304, y0 * 111263, z0, color='r', s=200, label='Estimated Explosion Point', marker='*')

ax.set_xlabel('X (meters)')
ax.set_ylabel('Y (meters)')
ax.set_zlabel('Z (meters)')
ax.set_title('3D Visualization of Selected Devices and Estimated Explosion Point')
ax.legend()

plt.show()
