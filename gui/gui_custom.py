import threading
import open3d as o3d
import customtkinter as ctk
import numpy as np

from gui.frames.text_frame import TextFrame
from gui.buttons.btn_open import BtnOpen
from gui.menu import Menu
from las_file_manager import LasFileManager
from model import CloudPointClassifier


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.model = None
        self.file_path = None

        ctk.set_appearance_mode('dark')

        # open as maximized window
        self.after(0, lambda: self.wm_state('zoomed'))
        self.title('Klasyfikator chmury punktów')

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='uniform')
        self.columnconfigure(1, weight=6, uniform='uniform')

        # widgets
        self.btn_open = BtnOpen(self, self.choose_file)

        self.mainloop()

    def choose_file(self, path):
        if path:
            self.btn_open.grid_forget()
            self.file_path = path
            self.start_after_choosing_file()

    def start_after_choosing_file(self):
        self.las_manager = LasFileManager(self.file_path)
        if self.model is None:
            self.model = CloudPointClassifier()
        self.menu = Menu(self, self.las_manager, self.model)
        self.panel = TextFrame(self, self.las_manager.class_informations())

    def update_frame_data(self):
        # Metoda do aktualizacji danych w klasie Frame

        new_data = self.las_manager.class_informations()
        self.panel.update_data(new_data)

    def disable_all(self):
        self.title('ładowanie')
        self.menu.configure(state='disabled')
        self.menu.disable()

    def enable_all(self):
        self.title('Klasyfikator chmury punktów')
        self.menu.configure(state='normal')
        self.menu.enable()
        self.update_frame_data()

# make visualization in another thread
    def visualize(self):
        thread = threading.Thread(target=self.visualize_in_thread)
        thread.start()

    # make visualization by class in another thread
    def visualize_color(self, color):
        thread = threading.Thread(target=self.visualize_classified, args=(color,))
        thread.start()

    def visualize_in_thread(self):
        o3d_points = self.las_manager.convert_to_o3d_data()

        if self.las_manager.points is not None:
            o3d.visualization.draw_geometries([o3d_points])
        else:
            print("Point cloud is not created yet.")

        self.enable_all()

# visualize selected classes
    def visualize_classified(self, selected_classes):
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

        masks = [self.las_manager.las_file.classification == c for c in selected_classes]

        pcd_o3d = o3d.geometry.PointCloud()

        for i, mask in enumerate(masks):
            xyz_t = np.vstack((self.las_manager.las_file.x[mask],
                               self.las_manager.las_file.y[mask], self.las_manager.las_file.z[mask]))
            pcd_temp = o3d.geometry.PointCloud()
            pcd_temp.points = o3d.utility.Vector3dVector(xyz_t.transpose())
            classification = selected_classes[i]
            if classification in classification_colors:
                color = classification_colors[classification]
            else:
                color = [0, 0, 0]
            pcd_temp.paint_uniform_color(color)
            pcd_o3d += pcd_temp

        pcd_center = pcd_o3d.get_center()

        pcd_o3d.translate(-pcd_center)

        o3d.visualization.draw_geometries([pcd_o3d])

        self.enable_all()
