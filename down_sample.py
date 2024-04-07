import laspy
import numpy as np
import open3d as o3d


class PointCloudDownSample:
    def __init__(self, input_file):
        self.input_file = input_file
        self.point_format = None

    def load_point_cloud(self):
        las_file = laspy.read(self.input_file)
        self.point_format = las_file.point_format
        points = np.vstack((las_file.x, las_file.y, las_file.z)).T
        colors = np.vstack((las_file.red, las_file.green, las_file.blue)).T
        self.point_cloud = o3d.geometry.PointCloud()
        self.point_cloud.points = o3d.utility.Vector3dVector(points)
        self.point_cloud.colors = o3d.utility.Vector3dVector(colors / 255.0)

    def clean_point_cloud(self, voxel_size=0.5):
        self.downsampled_point_cloud = self.point_cloud.voxel_down_sample(voxel_size)

    def save_point_cloud(self, output_file):
        downsampled_points = np.asarray(self.downsampled_point_cloud.points)
        downsampled_colors = np.asarray(self.downsampled_point_cloud.colors) * 255.0

        las_file_out = laspy.create(point_format=self.point_format, file_version="1.4")
        las_file_out.header = las_file_out.header
        las_file_out.x = downsampled_points[:, 0]
        las_file_out.y = downsampled_points[:, 1]
        las_file_out.z = downsampled_points[:, 2]
        las_file_out.red = downsampled_colors[:, 0].astype(np.uint16)
        las_file_out.green = downsampled_colors[:, 1].astype(np.uint16)
        las_file_out.blue = downsampled_colors[:, 2].astype(np.uint16)

        las_file_out.write(output_file)
