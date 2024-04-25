import numpy as np
import open3d as o3d
from pykdtree.kdtree import KDTree
import CSF


class PointCloudHeightNormalizer:
    def __init__(self, points, classes, cloth_resolution=0.01, voxel_size=0.1, k=8):
        self.classes = classes
        self.points = points
        self.voxel_size = voxel_size
        self.cloth_resolution = cloth_resolution
        self.k = k

    def normalize_height(self, ground_classes=None):
        if ground_classes is None:
            ground_points_indices, non_ground_points_indices = self.csf()
        else:
            ground_points_indices = np.where(np.isin(self.classes, ground_classes))[0]
            non_ground_points_indices = np.where(~np.isin(self.classes, ground_classes))[0]
        neighbors, reduce_ground_points = self.find_nearest_neighbors(ground_points_indices)

        min_heights = np.min(reduce_ground_points[:, 2][neighbors], axis=1)
        self.adjust_heights(min_heights, non_ground_points_indices, ground_points_indices)

    def downsample_points(self, indices):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.points[indices])
        downsampled_pcd = pcd.voxel_down_sample(self.voxel_size)
        return np.asarray(downsampled_pcd.points)

    def find_nearest_neighbors(self, ground_points_indices):
        reduce_ground_points = self.downsample_points(ground_points_indices)
        reduce_ground_points2 = reduce_ground_points[:, :2]
        non_ground_points = self.points[:, :2][~np.isin(np.arange(len(self.points)), ground_points_indices)]

        kd_tree = KDTree(reduce_ground_points2)
        dist, idx = kd_tree.query(non_ground_points, k=self.k)

        return idx, reduce_ground_points

    def csf(self):
        csf = CSF.CSF()
        csf.params.bSloopSmooth = False
        csf.params.cloth_resolution = self.cloth_resolution
        csf.setPointCloud(self.points)

        ground = CSF.VecInt()
        non_ground = CSF.VecInt()
        csf.do_filtering(ground, non_ground)

        ground = np.array(ground)
        non_ground = np.array(non_ground)

        self.classes[ground] = [2]
        self.classes[non_ground] = [1]

        return ground, non_ground

    def adjust_heights(self, min_heights, non_ground_points_indices, ground_points_indices):
        self.points[:, 2][non_ground_points_indices] -= min_heights
        self.points[:, 2][ground_points_indices] = 0
