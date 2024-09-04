import numpy as np
from itertools import combinations

# 设备数据：经度、纬度、高程
device_data = {
    'A': {'lon': 110.241, 'lat': 27.204, 'alt': 824},
    'B': {'lon': 110.783, 'lat': 27.456, 'alt': 727},
    'C': {'lon': 110.762, 'lat': 27.785, 'alt': 742},
    'D': {'lon': 110.251, 'lat': 28.025, 'alt': 850},
    'E': {'lon': 110.524, 'lat': 27.617, 'alt': 786},
    'F': {'lon': 110.467, 'lat': 28.081, 'alt': 678},
    'G': {'lon': 110.047, 'lat': 27.521, 'alt': 575}
}

# 经纬度转换为笛卡尔坐标
def convert_coordinates(lon, lat, alt):
    lat_to_m = 111263  # 纬度每度的距离，单位米
    lon_to_m = 97304   # 经度每度的距离，依赖纬度
    x = lon * lon_to_m
    y = lat * lat_to_m
    z = alt
    return x, y, z

# 计算四面体体积
def tetrahedron_volume(coords):
    A, B, C, D = coords
    AB = np.array(B) - np.array(A)
    AC = np.array(C) - np.array(A)
    AD = np.array(D) - np.array(A)
    volume = np.abs(np.dot(AB, np.cross(AC, AD))) / 6.0
    return volume

# 设备的笛卡尔坐标
device_coords = {key: convert_coordinates(val['lon'], val['lat'], val['alt']) for key, val in device_data.items()}

# 找出所有四个设备的组合
device_combinations = list(combinations(device_coords.keys(), 4))

# 计算每个组合的四面体体积
volumes = []
for combo in device_combinations:
    coords = [device_coords[device] for device in combo]
    volume = tetrahedron_volume(coords)
    volumes.append((combo, volume))

# 找出体积最大的组合
best_combination = max(volumes, key=lambda x: x[1])

# 输出结果
print(best_combination)
