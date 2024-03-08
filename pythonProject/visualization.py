import laspy
import open3d as o3d
import numpy as np

las_file_path = './../kortowo.las'
las_file = laspy.read(las_file_path)

xyz = np.column_stack((las_file.x, las_file.y, las_file.z))
colors = np.column_stack((las_file.red, las_file.green, las_file.blue)) / 65535.0

points = o3d.geometry.PointCloud()
points.points = o3d.utility.Vector3dVector(xyz)
if len(colors) == len(xyz):
    points.colors = o3d.utility.Vector3dVector(colors)

o3d.visualization.draw_geometries([points])
