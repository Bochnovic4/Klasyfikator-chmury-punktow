import threading

import numpy as np
import laspy
import customtkinter as ctk
from PIL import Image, ImageTk
import open3d as o3d

from gui.btn_open import *
from gui.menu import Menu
from las_file_manager import LasFileManager
from settings import *



class App(ctk.CTk):

    def __init__(self):
        super().__init__()
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
        self.btn_close = BtnClose(self, self.close_edit)
        self.menu = Menu(self, self.las_manager)
        self.panel = Frame(self, self.las_manager.class_informations())

    def update_frame_data(self):
        # Metoda do aktualizacji danych w klasie Frame
        new_data = self.las_manager.class_informations()
        self.panel.update_data(new_data)

    def close_edit(self):
        # hide everything
        self.btn_close.grid_forget()
        self.menu.grid_forget()

        # show open button
        self.btn_open = BtnOpen(self, self.choose_file)

    def disable_all(self):
        self.title('ładowanie')
        self.menu.configure(state='disabled')
        self.menu.disable()

    def enable_all(self):
        self.title('Klasyfikator chmury punktów')
        self.menu.configure(state='normal')
        self.menu.enable()
        self.update_frame_data()

    def visualize(self):
        def visualize_in_thread():
            # Convert LAS data to Open3D point cloud and visualize it.
            o3d_points = self.las_manager.covert_to_o3d_data()

            if self.las_manager.points is not None:
                o3d.visualization.draw_geometries([o3d_points])
            else:
                print("Point cloud is not created yet.")

            # Po zamknięciu okna Open3D, wywołaj funkcję enable_func, aby ponownie włączyć przyciski.
            self.enable_all()

        # Uruchomienie procesu w osobnym wątku
        thread = threading.Thread(target=visualize_in_thread)
        thread.start()

