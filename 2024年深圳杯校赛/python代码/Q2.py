import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设备数据：经度、纬度、高程
device_data = {
    'A': {'lon': 110.241, 'lat': 27.204, 'alt': 824, 'times': [100.767, 164.229, 214.850, 270.065]},
    'B': {'lon': 110.783, 'lat': 27.456, 'alt': 727, 'times': [92.453, 112.220, 169.362, 196.583]},
    'C': {'lon': 110.762, 'lat': 27.785, 'alt': 742, 'times': [75.560, 110.696, 156.936, 188.020]},
    'D': {'lon': 110.251, 'lat': 28.025, 'alt': 850, 'times': [94.653, 141.409, 196.517, 258.985]},
    'E': {'lon': 110.524, 'lat': 27.617, 'alt': 786, 'times': [78.600, 86.216, 118.443, 126.669]},
    'F': {'lon': 110.467, 'lat': 28.081, 'alt': 678, 'times': [67.274, 166.270, 175.482, 266.871]},
    'G': {'lon': 110.047, 'lat': 27.521, 'alt': 575, 'times': [103.738, 163.024, 206.789, 210.306]}
}

# 经纬度转换为笛卡尔坐标
def convert_coordinates(lon, lat, alt):
    lat_to_m = 111263  # 纬度每度的距离，单位米
    lon_to_m = 97304   # 经度每度的距离，依赖纬度
    x = lon * lon_to_m
    y = lat * lat_to_m
    z = alt
    return x, y, z

# 设备的笛卡尔坐标
device_coords = {key: convert_coordinates(val['lon'], val['lat'], val['alt']) for key, val in device_data.items()}

# 绘制三维空间中的设备分布
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制设备位置
for key, coords in device_coords.items():
    ax.scatter(*coords, label=f"Device {key}")

ax.set_xlabel('X (meters)')
ax.set_ylabel('Y (meters)')
ax.set_zlabel('Altitude (meters)')
ax.set_title('3D Visualization of Monitoring Devices')
ax.legend()

plt.show()

# 绘制音爆传播球体
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 生成球面的坐标数据
def draw_sphere(x_center, y_center, z_center, radius):
    phi = np.linspace(0, 2 * np.pi, 200)
    theta = np.linspace(0, np.pi, 200)
    phi, theta = np.meshgrid(phi, theta)
    x = x_center + radius * np.sin(theta) * np.cos(phi)
    y = y_center + radius * np.sin(theta) * np.sin(phi)
    z = z_center + radius * np.cos(theta)
    return x, y, z

# 颜色列表
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan']

# 声速
c = 340

# 绘制设备位置和对应的球体
for i, (key, coords) in enumerate(device_coords.items()):
    ax.scatter(*coords, label=f"Device {key}", s=100, color=colors[i])  # 设备位置
    for time in device_data[key]['times']:
        sphere_x, sphere_y, sphere_z = draw_sphere(*coords, time * c)
        ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color=colors[i], alpha=0.1)  # 球体表示音爆传播

ax.set_xlabel('X (meters)')
ax.set_ylabel('Y (meters)')
ax.set_zlabel('Altitude (meters)')
ax.set_title('3D Visualization of Monitoring Devices and Shockwave Spheres')
ax.legend()

plt.show()



