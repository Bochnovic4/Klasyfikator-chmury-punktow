import laspy
import open3d as o3d
import numpy as np

las_file_path = './../WMII.las'
las_file = laspy.read(las_file_path)

xyz = np.column_stack((las_file.x, las_file.y, las_file.z))
colors = np.column_stack((las_file.red, las_file.green, las_file.blue)) / 65535.0

points = o3d.geometry.PointCloud()
points.points = o3d.utility.Vector3dVector(xyz)
if len(colors) == len(xyz):
    points.colors = o3d.utility.Vector3dVector(colors)

# statistical_outlier
# cl, ind = points.remove_statistical_outlier(nb_neighbors=10, std_ratio=10.0)
# radius_outlier
cl, ind = points.remove_radius_outlier(nb_points=10, radius=1)

# create filtered point cloud
points = points.select_by_index(ind)

# Create a new LAS file
header = laspy.LasHeader(version="1.4", point_format=2)
header.x_scale = 0.01
header.y_scale = 0.01
header.z_scale = 0.01
las = laspy.LasData(header)

las.x = np.asarray(points.points)[:, 0]
las.y = np.asarray(points.points)[:, 1]
las.z = np.asarray(points.points)[:, 2]

las.red = np.asarray(points.colors)[:, 0].T * 65535.0
las.green = np.asarray(points.colors)[:, 1].T * 65535.0
las.blue = np.asarray(points.colors)[:, 2].T * 65535.0

# Write the LAS file to disk
las.write("./WMII_filtered.las")


# create point cloud from removed points and sets their color to red
# removed_points = points.select_by_index(ind,invert=True)
# removed_points.paint_uniform_color([1, 0, 0])


o3d.visualization.draw_geometries([points])