import threading
import tkinter as tk
import laspy
import numpy as np
import open3d as o3d


class LasFileManager:
    def __init__(self, file_path, labels=None):
        self.file_path = file_path
        self.las_file = laspy.read(self.file_path)
        self.points = np.column_stack((self.las_file.x, self.las_file.y, self.las_file.z))
        self.colors = np.column_stack((self.las_file.red, self.las_file.green, self.las_file.blue))
        self.classes = np.asarray(self.las_file.classification)
        self.ground_points_indices = np.where(np.isin(self.classes, [11, 17, 25]))[0]
        self.ball_density = None
        self.cylinder_density = None
        self.phi_angles_of_normal_vectors = None
        self.theta_angles_of_normal_vectors = None

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

    def visualize(self, indices=None):
        if indices is None:
            o3d_points = self.convert_to_o3d_data()
        else:
            o3d_points = self.convert_to_o3d_data(indices)

        if o3d_points.points:
            o3d.visualization.draw_geometries([o3d_points])
        else:
            print("Point cloud is not created yet.")

    def filter_points(self, nb_neighbors=20, std_ratio=10.0, invert=False):
        # Filter out noise from the point cloud using statistical outlier removal.
        o3d_points = self.convert_to_o3d_data()

        # Perform the statistical outlier removal.
        cl, ind = o3d.geometry.PointCloud.remove_statistical_outlier(o3d_points, nb_neighbors=nb_neighbors,
                                                                     std_ratio=std_ratio)
        # Select the points that remain after filtering.
        o3d_points = o3d_points.select_by_index(ind, invert=invert)
        # Update the class's point, color, and classification data with the filtered results.
        self.points = np.asarray(o3d_points.points)
        self.classes = self.classes[ind]
        colors_array = np.asarray(o3d_points.colors) * 65535
        self.colors = colors_array.astype(np.uint16)
        self.ground_points_indices = np.where(np.isin(self.classes, [11, 17, 25]))[0]
        self.non_ground_points_indices = np.where(np.isin(self.classes, [0, 1, 13, 15, 19]))[0]

    def color_classified(self):
        classification_colors = settings.LABEL_COLORS
        colors = np.zeros((len(self.points), 3))
        
        for classification, color in classification_colors.items():
            indices = self.classes == classification
            colors[indices] = np.asarray(color) * 65535
            
        self.colors = colors.astype(np.uint16)

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
            raise ValueError("Obiekty muszą mieć tę samą liczbę punktów do porównania")

        correct_classifications = self.classes == self.las_file.classes
        total_correct = np.sum(correct_classifications)
        total_points = len(self.classes)
        accuracy = total_correct / total_points

        result = f"Liczba poprawnie sklasyfikowanych punktów: {total_correct}/{total_points} ({accuracy:.2%})\n"

        unique_classes = np.unique(self.classes)
        for cls in unique_classes:
            cls_mask = self.classes == cls
            correct_per_class = np.sum(correct_classifications[cls_mask])
            total_per_class = np.sum(cls_mask)
            accuracy_per_class = correct_per_class / total_per_class if total_per_class else 0
            result += (
                f"Klasa {cls}: Poprawnie sklasyfikowane "
                f"{correct_per_class}/{total_per_class} ({accuracy_per_class:.2%})\n")

        return result

    def set_density(self):
        def density(points, radius):
            tree = spatial.cKDTree(points)

            neighbors = tree.query_ball_tree(tree, radius)
            frequency = np.array([len(sublist) for sublist in neighbors])

            min_val = np.min(frequency)
            max_val = np.max(frequency)

            normalized_frequency = (frequency - min_val) / (max_val - min_val)

            return normalized_frequency

        self.ball_density = density(self.points, 0.2)
        self.cylinder_density = density(self.points[:, :2], 0.05)

    def set_angles_of_normal_vectors(self):
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

        self.phi_angles_of_normal_vectors = phi_angles
        self.theta_angles_of_normal_vectors = theta_angles
    
    def __str__(self):
        return str(self.las_file)
