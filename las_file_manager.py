import scipy.spatial as spatial
import settings
import laspy
import numpy as np
import open3d as o3d
import height_normalization


class LasFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.las_file = laspy.read(self.file_path)
        self.points = np.column_stack((self.las_file.x, self.las_file.y, self.las_file.z))
        self.colors = np.column_stack((self.las_file.red, self.las_file.green, self.las_file.blue))
        self.classes = np.asarray(self.las_file.classification)

    def write_las(self, output_path):
        # Create a new LAS file with the same version and point format as the input file.
        version = self.las_file.header.version
        point_format = self.las_file.header.point_format
        header = laspy.LasHeader(version=version, point_format=point_format)
        las = laspy.LasData(header)

        las.x, las.y, las.z = np.asarray(self.points).T
        las.red, las.green, las.blue = np.asarray(self.colors).T
        las.classification = np.asarray(self.classes)

        las.write(output_path)

    def convert_to_o3d_data(self, indices=None):
        o3d_points = o3d.geometry.PointCloud()

        if indices is None:
            points = self.points
            colors = self.colors
        else:
            points = self.points[indices]
            colors = self.colors[indices]

        o3d_points.points = o3d.utility.Vector3dVector(points)
        o3d_points.colors = o3d.utility.Vector3dVector(colors / 65535.0)

        return o3d_points

    def visualize(self, indices=None, classes=None):
        if classes is not None:
            indices = np.where(np.isin(self.classes, classes))[0]

        if indices is None:
            o3d_points = self.convert_to_o3d_data()
        else:
            o3d_points = self.convert_to_o3d_data(indices)

        if o3d_points.points:
            o3d.visualization.draw_geometries([o3d_points])
        else:
            return "Point cloud is not created yet."

    def filter_points(self, nb_neighbors=20, std_ratio=5.0, invert=False):
        o3d_points = self.convert_to_o3d_data()
        cl, ind = o3d.geometry.PointCloud.remove_statistical_outlier(o3d_points, nb_neighbors=nb_neighbors,
                                                                     std_ratio=std_ratio)
        o3d_points = o3d_points.select_by_index(ind, invert=invert)

        self.points = np.asarray(o3d_points.points)
        self.classes = self.classes[ind]

        colors_array = np.asarray(o3d_points.colors) * 65535
        self.colors = colors_array.astype(np.uint16)

        return ind

    def color_classified(self, selected_classes=None):
        classification_colors = settings.LABEL_COLORS
        colors = np.zeros((len(self.points), 3))

        for classification, color in classification_colors.items():
            indices = self.classes == classification
            colors[indices] = np.asarray(color) * 65535

        self.colors = colors.astype(np.uint16)
        if selected_classes is not None:
            self.visualize(classes=selected_classes)

    def color_normalized_array(self, array):
        def get_color(value):
            if value < 0.5:
                # Map from blue to green
                green = 2 * value
                blue = 1 - green
                red = 0
            else:
                # Map from green to red
                red = (value - 0.5) * 2
                green = 1 - red
                blue = 0
            return red, green, blue

        min_val, max_val = array.min(), array.max()
        normalized_array = (array - min_val) / (max_val - min_val)
        colors = np.array([get_color(value) for value in normalized_array])
        self.colors[:, 0] = colors[:, 0] * 65535.0
        self.colors[:, 1] = colors[:, 1] * 65535.0
        self.colors[:, 2] = colors[:, 2] * 65535.0

    def class_informations(self):
        result = {
            "Liczba punktów":
                str(len(self.points)),
            "klasyfikacje":
                str(np.unique(self.classes)),
            "min x":
                str(np.min(self.points[:, 0])),
            "max x":
                str(np.max(self.points[:, 0])),
            "min y":
                str(np.min(self.points[:, 1])),
            "max y":
                str(np.max(self.points[:, 1])),
            "min z":
                str(np.min(self.points[:, 2])),
            "max z":
                str(np.max(self.points[:, 2])),
        }
        return result

    def file_informations(self):
        result = {
            "nazwy wymiarów pliku LAS":
                str(list(self.las_file.point_format.dimension_names)),
            "Format pliku LAS":
                str(self.las_file.header.version),
            "Format punktów":
                str(self.las_file.header.version),
            "Liczba punktów":
                str(len(self.las_file.points)),
            "klasyfikacje":
                str(np.unique(self.las_file.classification)),
            "min x":
                str(self.las_file.header.x_min),
            "max x":
                str(self.las_file.header.x_max),
            "min y":
                str(self.las_file.header.y_min),
            "max y":
                str(self.las_file.header.y_max),
            "min z":
                str(self.las_file.header.z_min),
            "max z":
                str(self.las_file.header.z_max),
            "min intensywność":
                str(np.min(self.las_file.intensity)),
            "max intensywność":
                str(np.max(self.las_file.intensity)),
            "średnia intensywność":
                str(np.mean(self.las_file.intensity)),
        }
        return result

    def compare_classifications(self):
        if len(self.classes) != len(self.las_file.classes):
            return "Obiekty muszą mieć tę samą liczbę punktów do porównania"

        correct_classifications = self.classes == self.las_file.classes
        total_correct = np.sum(correct_classifications)
        total_points = len(self.classes)
        accuracy = total_correct / total_points

        result = f"Liczba poprawnie sklasyfikowanych punktów: {total_correct}/{total_points} ({accuracy:.2%})\n"

        unique_classes = np.unique(self.classes)
        for cls in unique_classes:
            cls_mask = self.classes == cls
            correct_per_class = np.sum(cls_mask & correct_classifications)
            total_per_class = np.sum(cls_mask)
            accuracy_per_class = correct_per_class / total_per_class if total_per_class else 0
            result += (
                f"Klasa {cls}: Poprawnie sklasyfikowane "
                f"{correct_per_class}/{total_per_class} ({accuracy_per_class:.2%})\n")

        return result

    def set_frequency(self):
        def get_frequency_of_neighbors(points, radius):
            tree = spatial.cKDTree(points)

            neighbors = tree.query_ball_tree(tree, radius)
            frequency_of_neighbors = np.array([len(sublist) for sublist in neighbors])

            return frequency_of_neighbors

        cylinder_density = get_frequency_of_neighbors(self.points[:, :2], 0.05)

        return cylinder_density

    def set_normal_vectors(self):
        def calculate_phi_angle_of_normals(vertex_normals):
            z_axis = vertex_normals[:, 2]
            normal_vector_length = np.linalg.norm(vertex_normals)
            angle = np.arccos(z_axis / normal_vector_length)
            return angle

        def calculate_theta_angle_of_normals(vertex_normals):
            x = vertex_normals[:, 0]
            y = vertex_normals[:, 1]
            angle = np.arctan(y, x)

            return angle

        o3d_points = self.convert_to_o3d_data()
        o3d_points.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=100))
        o3d_points.orient_normals_to_align_with_direction()
        vertex_normals = np.asarray(o3d_points.normals)

        phi_angles = calculate_phi_angle_of_normals(vertex_normals)
        theta_angles = calculate_theta_angle_of_normals(vertex_normals)

        phi_angles_of_normal_vectors = phi_angles
        theta_angles_of_normal_vectors = theta_angles

        return phi_angles_of_normal_vectors, theta_angles_of_normal_vectors, vertex_normals[:, 0], vertex_normals[:, 1], vertex_normals[:, 2]

    def get_model_values(self, ground_classes=None):
        ind = self.filter_points()
        cylinder_density = self.set_frequency()
        phi_angles_of_normal_vectors, theta_angles_of_normal_vectors, normal_vectors_x, normal_vectors_y, normal_vectors_z = self.set_normal_vectors()
        normalized_points = self.normalize_height(ground_classes=ground_classes)
        min_height, max_height, mean_height = self.set_min_max_mean_height(normalized_points)
        return [
            normalized_points[:, 2],
            self.las_file.intensity[ind],
            self.las_file.number_of_returns[ind],
            self.las_file.return_number[ind],
            cylinder_density,
            normal_vectors_x,
            normal_vectors_y,
            normal_vectors_z,
            min_height,
            max_height,
            mean_height
        ]


    def csf(self, cloth_resolution=1):
        height_normalizer = height_normalization.PointCloudHeightNormalizer(self.points.copy(),
                                                                            self.classes.copy(),
                                                                            cloth_resolution=cloth_resolution)
        height_normalizer.csf()
        classes = height_normalizer.classes
        self.classes = classes

    def normalize_height(self, voxel_size=0.1, k=8, cloth_resolution=1, ground_classes=None):
        height_normalizer = height_normalization.PointCloudHeightNormalizer(self.points.copy(),
                                                                            self.classes.copy(),
                                                                            cloth_resolution=cloth_resolution,
                                                                            voxel_size=voxel_size,
                                                                            k=k)

        height_normalizer.normalize_height(ground_classes)
        normalized_points = height_normalizer.points

        return normalized_points

    def downsample_points(self, voxel_size=1, indices=None):
        if indices is None:
            indices = np.arange(len(self.points))
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.points[indices])
        pcd.colors = o3d.utility.Vector3dVector(self.colors[indices])

        downsampled_pcd = pcd.voxel_down_sample(voxel_size)

        reduced_points = np.asarray(downsampled_pcd.points)
        reduced_colors = np.asarray(downsampled_pcd.colors)

        return reduced_points, reduced_colors

    def set_min_max_mean_height(self, normalized_points):
        points = normalized_points[:, :2]
        tree = spatial.cKDTree(points)
        neighbors = tree.query_ball_tree(tree, 0.05)

        num_neighbors = np.array([len(sublist) for sublist in neighbors])

        flattened_indices = np.concatenate(neighbors)
        heights = normalized_points[flattened_indices, 2]

        indices = np.concatenate(([0], np.cumsum(num_neighbors)[:-1]))
        min_height = np.minimum.reduceat(heights, indices)
        max_height = np.maximum.reduceat(heights, indices)
        sum_height = np.add.reduceat(heights, indices)

        mean_height = sum_height / num_neighbors

        return min_height, max_height, mean_height
