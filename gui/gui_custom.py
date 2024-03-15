import numpy as np
import laspy
import customtkinter as ctk
from PIL import Image, ImageTk
import open3d as o3d

from gui.btn_open import *
from las_file_manager import LasFileManager
from settings import *
from menu import Menu


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

    def close_edit(self):
        # hide everything
        self.btn_close.grid_forget()
        self.menu.grid_forget()

        # show open button
        self.btn_open = BtnOpen(self, self.choose_file)


App()
