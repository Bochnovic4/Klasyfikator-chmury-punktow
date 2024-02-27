import laspy
import open3d as o3d
import numpy as np

las_file_path = 'WMII.las'
las_file = laspy.file.File(las_file_path, mode='r')


xyz = np.vstack((las_file.x, las_file.y, las_file.z)).T
colors = np.vstack((las_file.red, las_file.green, las_file.blue)).T / 65535.0

points = o3d.geometry.PointCloud()
points.points = o3d.utility.Vector3dVector(xyz)

if colors.shape[0] == xyz.shape[0]:
    points.colors = o3d.utility.Vector3dVector(colors)


las_file.close()

o3d.visualization.draw_geometries([points])
