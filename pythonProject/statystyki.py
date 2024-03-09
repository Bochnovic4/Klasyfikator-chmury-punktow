import laspy
import numpy as np

# Wczytanie pliku LAS
las_file_path = './WMII_CLASS.las'
las = laspy.read(las_file_path)

# Informacje ogólne
print(f"nazwy wymiarów pliku LAS: {list(las.point_format.dimension_names)}")
print(f"nazwy podstawowych wymiarów pliku LAS: {list(las.point_format.standard_dimension_names)}")
print(f"nazwy dodatkowych wymiarów pliku LAS: {list(las.point_format.extra_dimension_names)}")
print(f"Format pliku LAS: {las.header.version}")
print(f"Format punktów: {las.header.point_format.id}")
print(f"Liczba punktów: {len(las.points)}")
print(f"sklasyfikowane punkty: {np.unique(las.classification)}")
print(f"Zakres X: min = {las.header.x_min}, max = {las.header.x_max}")
print(f"Zakres Y: min = {las.header.y_min}, max = {las.header.y_max}")
print(f"Zakres Z: min = {las.header.z_min}, max = {las.header.z_max}")
print(f"Intensywność: min = {np.min(las.intensity)}, max = {np.max(las.intensity)}, średnia = {np.mean(las.intensity)}")
