import customtkinter as ctk
from btn_open import *
from las_file_manager import LasFileManager


class Menu(ctk.CTkTabview):
    def __init__(self, parent, las_manager):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        # tabs
        self.add('Działaj')
        self.add('Zapisz')

        # widgets
        WorkFrame(self.tab('Działaj'), parent, las_manager)
        SaveFrame(self.tab('Zapisz'), parent, las_manager)


class WorkFrame(ctk.CTkFrame):
    def __init__(self, parent, parents_parent, las_manager):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        BtnVisualize(self, las_manager.visualize)
        BtnCreator(self, "Usuń szum", las_manager.filter_points)


class SaveFrame(ctk.CTkFrame):
    def __init__(self, parent, parents_parent, las_manager):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        BtnSave(self, las_manager.write_las, parents_parent.file_path)
        BtnSaveAs(self,las_manager.write_las)
