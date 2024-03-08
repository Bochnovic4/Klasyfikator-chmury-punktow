import laspy
import open3d as o3d
import numpy as np

las_file_path = './WMII_CLASS.las'
las_file = laspy.read(las_file_path)

xyz = np.column_stack((las_file.x, las_file.y, las_file.z))

points = o3d.geometry.PointCloud()
points.points = o3d.utility.Vector3dVector(xyz)

classifications = las_file.classification

# Przygotowanie kolorów dla klasyfikacji
classification_colors = {
    0: [0, 0, 1],    # szum: Niebieski
    1: [0.6, 0.4, 0],    # niesklasyfikowane: Brązowy
    11: [0, 1, 0],         # trawa: zielony
    13: [0, 0.3, 0],   # nw co to jest: Ciemnozielony
    15: [0.65, 0.50, 0.39],# Budynki: Orzechowy
    17: [0.3, 0.3, 0.3],     # ulica: Ciemnoszary
    19: [1, 0, 0],         # Przewody: Czerwony
    25: [0.85, 0.85, 0.85] # droga: Szary
}

# Inicjalizacja tablicy kolorów dla każdego punktu
colors = np.zeros((len(las_file.points), 3))

# Przypisanie kolorów na podstawie klasyfikacji
for classification, color in classification_colors.items():
    indices = las_file.classification == classification
    colors[indices] = color

# Ustawienie kolorów dla chmury punktów
points.colors = o3d.utility.Vector3dVector(colors)

# Wizualizacja
o3d.visualization.draw_geometries([points])
