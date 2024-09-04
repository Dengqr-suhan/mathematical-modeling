import numpy as np
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt
import pandas as pd

# 设备数据：经度、纬度、高程、音爆抵达时间
device_data = {
    'A': {'lon': 110.241, 'lat': 27.204, 'alt': 824, 'times': [100.767, 164.229, 214.850, 270.065]},
    'B': {'lon': 110.783, 'lat': 27.456, 'alt': 727, 'times': [92.453, 112.220, 169.362, 196.583]},
    'C': {'lon': 110.762, 'lat': 27.785, 'alt': 742, 'times': [75.560, 110.696, 156.936, 188.020]},
    'D': {'lon': 110.251, 'lat': 28.025, 'alt': 850, 'times': [94.653, 141.409, 196.517, 258.985]},
    'E': {'lon': 110.524, 'lat': 27.617, 'alt': 786, 'times': [78.600, 86.216, 118.443, 126.669]},
    'F': {'lon': 110.467, 'lat': 28.081, 'alt': 678, 'times': [67.274, 166.270, 175.482, 266.871]},
    'G': {'lon': 110.047, 'lat': 27.521, 'alt': 575, 'times': [103.738, 163.024, 206.789, 210.306]}
}

# 假设真实的残骸位置和时间
true_debris_data = [
    {'lon': 110.450, 'lat': 27.700, 'alt': 800, 'time': 55},
    {'lon': 110.470, 'lat': 27.690, 'alt': 850, 'time': 56},
    {'lon': 110.480, 'lat': 27.680, 'alt': 900, 'time': 57},
    {'lon': 110.490, 'lat': 27.670, 'alt': 950, 'time': 58}
]

# 设定最大速度 m/s
v_max = 3000
# 声速 m/s
c = 340

# 经纬度转换为笛卡尔坐标
def convert_coordinates(lon, lat, alt):
    lat_to_m = 111263  # 纬度每度的距离，单位米
    lon_to_m = 97304   # 经度每度的距离，依赖纬度
    x = lon * lon_to_m
    y = lat * lat_to_m
    z = alt
    return x, y, z

# 笛卡尔坐标转换为地理坐标
def cartesian_to_geographic(x, y, z):
    lat_to_m = 111263  # 纬度每度的距离，单位米
    lon_to_m = 97304   # 经度每度的距离，依赖纬度
    lon = x / lon_to_m
    lat = y / lat_to_m
    alt = z
    return lon, lat, alt

# 设备的笛卡尔坐标和时间
device_coords = {key: convert_coordinates(val['lon'], val['lat'], val['alt']) for key, val in device_data.items()}
device_times = {key: val['times'] for key, val in device_data.items()}

# 目标函数
def objective_function(vars):
    errors = 0
    base_time = vars[3]  # 所有残骸时间的基准点
    for j in range(4):  # 对每个残骸进行计算
        x, y, z, t = vars[j * 4:(j + 1) * 4]
        
        # 添加时间差惩罚
        if np.abs(t - base_time) > 5:
            errors += 10000 * (np.abs(t - base_time) - 5)

        # 添加速度约束
        if j > 0:
            x_prev, y_prev, z_prev, t_prev = vars[(j - 1) * 4:j * 4]
            dist = np.sqrt((x - x_prev) ** 2 + (y - y_prev) ** 2 + (z - z_prev) ** 2)
            time_diff = np.abs(t - t_prev)
            if time_diff > 0 and (dist / time_diff) > v_max:
                errors += 100000 * ((dist / time_diff) - v_max)
                
            # 添加高度递增约束
            if z <= z_prev:
                errors += 100000 * (z_prev - z)  # 惩罚非递增的高度

        # 计算时间误差
        for key, value in device_coords.items():
            x_i, y_i, z_i = value
            predicted_time = t + np.sqrt((x - x_i) ** 2 + (y - y_i) ** 2 + (z - z_i) ** 2) / c
            actual_time = device_times[key][j]
            errors += (predicted_time - actual_time) ** 2  # 累加预测时间和实际时间的误差平方
    
    return errors

# 禁忌搜索辅助函数
class TabuSearch:
    def __init__(self, tabu_size=10):
        self.tabu_list = []
        self.tabu_size = tabu_size

    def add_to_tabu_list(self, solution):
        if len(self.tabu_list) >= self.tabu_size:
            self.tabu_list.pop(0)
        self.tabu_list.append(solution)

    def is_in_tabu_list(self, solution):
        return any(np.allclose(solution, s) for s in self.tabu_list)

# 自定义的差分进化优化器，结合禁忌搜索
def differential_evolution_with_tabu(func, bounds, tabu_size=10, **kwargs):
    tabu_search = TabuSearch(tabu_size)
    result = differential_evolution(func, bounds, **kwargs)
    
    # 如果找到的解在禁忌列表中，则重新优化
    while tabu_search.is_in_tabu_list(result.x):
        result = differential_evolution(func, bounds, **kwargs)
    
    # 将新解加入禁忌列表
    tabu_search.add_to_tabu_list(result.x)
    
    return result

# 边界设置
bounds = [(0, 2e7), (0, 2e7), (500, 1000), (50, 300)] * 4

# 差分进化优化，结合禁忌搜索
result = differential_evolution_with_tabu(
    objective_function, bounds, tabu_size=10, strategy='best1bin', maxiter=10000, popsize=20, tol=0.01, mutation=(0.5, 1),
    recombination=0.7)

# 判断优化是否成功
if result.success:
    print("Optimization successful.")
    optimized_vars = result.x.reshape(4, 4)  # 将优化结果重塑为 4 行 (x, y, z, t)
    debris_coords = [cartesian_to_geographic(*vars[:3]) for vars in optimized_vars]  # 转换坐标为地理坐标

    # 绘制监测设备位置和优化后的残骸位置
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制设备位置
    device_cartesian = {key: convert_coordinates(val['lon'], val['lat'], val['alt']) for key, val in device_data.items()}
    for key, coords in device_cartesian.items():
        ax.scatter(*coords, label=f"Device {key}")

    # 绘制优化得到的残骸位置
    for idx, coords in enumerate(debris_coords):
        ax.scatter(*coords[:3], marker='^', label=f"Debris {idx+1}")

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude')
    ax.set_title('3D Visualization of Optimized Debris Locations and Monitoring Devices')
    ax.legend()

    plt.show()

    # 计算误差并输出
    total_position_error = 0
    total_time_error = 0

    print("Error analysis:")
    results_list = []
    for i, vars in enumerate(optimized_vars, 1):
        x, y, z, t = vars
        lon, lat, alt = cartesian_to_geographic(x, y, z)
        
        # 计算与真实数据的误差
        true_data = true_debris_data[i - 1]
        position_error = np.sqrt((lon - true_data['lon']) ** 2 + (lat - true_data['lat']) ** 2 + (alt - true_data['alt']) ** 2)
        time_error = np.abs(t - true_data['time'])
        
        total_position_error += position_error
        total_time_error += time_error
        
        print(f"Debris {i}:")
        print(f"  Predicted Longitude = {lon:.6f}°, Latitude = {lat:.6f}°, Altitude = {alt:.2f} meters, Time = {t:.2f} seconds")
        print(f"  True Longitude = {true_data['lon']:.6f}°, Latitude = {true_data['lat']:.6f}°, Altitude = {true_data['alt']:.2f} meters, Time = {true_data['time']:.2f} seconds")
        print(f"  Position Error = {position_error:.6f} meters, Time Error = {time_error:.2f} seconds")
        
        # 保存结果到列表
        results_list.append({
            'Debris Index': i,
            'Predicted Longitude': lon,
            'Predicted Latitude': lat,
            'Predicted Altitude': alt,
            'Predicted Time': t,
            'True Longitude': true_data['lon'],
            'True Latitude': true_data['lat'],
            'True Altitude': true_data['alt'],
            'True Time': true_data['time'],
            'Position Error': position_error,
            'Time Error': time_error
        })
    
    print(f"\nTotal Position Error: {total_position_error:.6f} meters")
    print(f"Total Time Error: {total_time_error:.2f} seconds")

    # 保存到CSV文件
    df = pd.DataFrame(results_list)
    df.to_csv('Q2_optimized_debris_results.csv', index=False)
    print("Results saved to optimized_debris_results.csv")

else:
    print("Optimization failed:", result.message)
