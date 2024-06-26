import customtkinter as ctk

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
