import threading
import tkinter as tk
import laspy
import numpy as np
import open3d as o3d


class LasFileManager:
    def __init__(self, file_path, labels=None):
        # Initialize the class with the path to a LAS file.
        self.file_path = file_path
        # Read the LAS file using laspy.
        self.las_file = laspy.read(self.file_path)
        # Extract coordinates (x, y, z) of points from the LAS file and stack them into a numpy array.
        self.points = np.column_stack((self.las_file.x, self.las_file.y, self.las_file.z))
        # Extract RGB colors of points from the LAS file and stack them into a numpy array.
        self.colors = np.column_stack((self.las_file.red, self.las_file.green, self.las_file.blue))
        # Convert the classification of each point into a numpy array.
        self.classes = labels if labels is not None else np.asarray(self.las_file.classification)

    def write_las(self, output_path):
        # Create a new LAS file with the same version and point format as the input file.
        version = self.las_file.header.version
        point_format = self.las_file.header.point_format
        header = laspy.LasHeader(version=version, point_format=point_format)
        las = laspy.LasData(header)

        # Populate the new LAS file with modified point coordinates and colors.
        las.x, las.y, las.z = np.asarray(self.points).T
        las.red, las.green, las.blue = np.asarray(self.colors).T
        # Populate the new LAS file with modified classifications.
        las.classification = np.asarray(self.classes)

        # Write the modified LAS data to the specified output path.
        las.write(output_path)

    def covert_to_o3d_data(self):
        # Convert LAS point data to an Open3D point cloud format.
        o3d_points = o3d.geometry.PointCloud()
        o3d_points.points = o3d.utility.Vector3dVector(self.points)
        # If color data is available, convert and set the colors for the Open3D point cloud.
        if len(self.colors) == len(self.points):
            o3d_points.colors = o3d.utility.Vector3dVector(self.colors / 65535.0)

        return o3d_points

    def filter_points(self, nb_neighbors=20, std_ratio=10.0, invert=False):
        # Filter out noise from the point cloud using statistical outlier removal.
        o3d_points = self.covert_to_o3d_data()

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

    def color_classified(self):
        classification_colors = {
            0: [0, 0, 1],  # szum: Niebieski
            1: [0.6, 0.4, 0],  # niesklasyfikowane: Brązowy
            11: [0, 1, 0],  # trawa: zielony
            13: [0, 0.3, 0],  # nw co to jest: Ciemnozielony
            15: [0.65, 0.50, 0.39],  # Budynki: Orzechowy
            17: [0.3, 0.3, 0.3],  # ulica: Ciemnoszary
            19: [1, 0, 0],  # Przewody: Czerwony
            25: [0.85, 0.85, 0.85]  # droga: Szary
        }

        # Initialize the color array for each point
        colors = np.zeros((len(self.las_file.points), 3))
        for classification, color in classification_colors.items():
            indices = self.las_file.classification == classification
            colors[indices] = np.asarray(color) * 65535

        self.colors = colors.astype(np.uint16)

    def class_informations(self):
        result = {
            "Liczba punktów":
                str(len(self.points)),
            "klasyfikacje":
                str(np.unique(self.classes)),
            "min x":
                str(np.min(self.points[0:])),
            "max x":
                str(np.max(self.points[0:])),
            "min y":
                str(np.min(self.points[1:])),
            "max y":
                str(np.max(self.points[1:])),
            "min z":
                str(np.min(self.points[2:])),
            "max z":
                str(np.max(self.points[2:])),
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

    def compare_classifications(self, other):
        if not isinstance(other, LasFileManager):
            raise ValueError("Argument musi być instancją LasFileManager")

        if len(self.classes) != len(other.classes):
            raise ValueError("Obiekty muszą mieć tę samą liczbę punktów do porównania")

        correct_classifications = self.classes == other.classes
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
    def __str__(self):
        return str(self.las_file)
