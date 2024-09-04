import numpy as np
# 震动波传播速度 (m/s)
v = 340
# 监测设备的数据：经度(°), 纬度(°), 高程(m), 音爆到达时间(s)
# A, B, C, D, E, F, G
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

# 带动量的梯度下降法
def gradient_descent_with_momentum(selected_data, initial_guess, learning_rate=1e-6, max_iter=100, tolerance=1e-6, momentum=0.9):
    vars = np.array(initial_guess)
    velocity = np.zeros_like(vars)
    for iteration in range(max_iter):
        grad = np.zeros_like(vars)
        h = 1e-5  # 用于计算数值梯度的微小偏移量
        for i in range(len(vars)):
            vars_plus_h = np.copy(vars)
            vars_plus_h[i] += h
            grad[i] = (objective_function(vars_plus_h, selected_data) - objective_function(vars, selected_data)) / h
        
        # 使用动量更新变量
        velocity = momentum * velocity - learning_rate * grad
        new_vars = vars + velocity
        
        # 检查是否收敛
        if np.linalg.norm(new_vars - vars) < tolerance:
            break
        
        vars = new_vars
    
    return vars

# 初始猜测值 (x0, y0, z0, t0)
initial_guess = [110.5, 27.5, 800, 10]

# 使用随机选择和梯度下降法求解
best_solution = None
best_error = float('inf')
num_trials = 100  # 尝试次数

for _ in range(num_trials):
    # 随机选择4个不同的监测设备数据
    indices = np.random.choice(data.shape[0], 4, replace=False)
    selected_data = data[indices]
    
    # 多次随机初始化
    random_guess = initial_guess + np.random.normal(0, 0.1, size=4)
    solution = gradient_descent_with_momentum(selected_data, random_guess)
    
    # 计算当前解的误差
    current_error = objective_function(solution, selected_data)
    if current_error < best_error:
        best_error = current_error
        best_solution = solution

# 输出最佳结果
x0, y0, z0, t0 = best_solution
print(f"音爆发生位置经度: {x0:.6f}°")
print(f"音爆发生位置纬度: {y0:.6f}°")
print(f"音爆发生位置高程: {z0:.2f}米")
print(f"音爆发生时间: {t0:.3f}秒")

# 使用所有设备验证最佳解
total_error = 0
for i in range(data.shape[0]):
    lon_i, lat_i, z_i, t_i = data[i]
    dx, dy = lon_lat_to_distance(lon_i, lat_i, x0, y0)
    dz = z_i - z0
    distance = np.sqrt(dx**2 + dy**2 + dz**2)
    t_pred = t0 + distance / v
    error = t_pred - t_i
    total_error += error ** 2
    print(f"设备 {i+1} 的预测到达时间: {t_pred:.3f}秒，实际到达时间: {t_i:.3f}秒，误差: {error:.3f}秒")

print(f"总误差平方和: {total_error:.6f}")
