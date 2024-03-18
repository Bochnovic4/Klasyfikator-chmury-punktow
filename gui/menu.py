import customtkinter as ctk

from gui.btn_open import *
from las_file_manager import LasFileManager


class Menu(ctk.CTkTabview):
    def __init__(self, parent, las_manager):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        # tabs
        self.add('Działaj')
        self.add('Zapisz')

        # widgets
        self.work_frame = WorkFrame(self.tab('Działaj'), parent, las_manager)
        self.save_frame = SaveFrame(self.tab('Zapisz'), parent, las_manager)

    def disable(self):
        self.work_frame.disable()
        self.save_frame.disable()

    def enable(self):
        self.work_frame.enable()
        self.save_frame.enable()


class WorkFrame(ctk.CTkFrame):
    def __init__(self, parent, parents_parent, las_manager):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.btn_visualize = BtnVisualize(self, parents_parent.visualize, parents_parent.disable_all)
        self.btn_filter_points = BtnCreator(self, "Usuń szum", las_manager.filter_points, parents_parent.disable_all,
                                            parents_parent.enable_all)

    def disable(self):
        self.btn_visualize.configure(state='disabled')
        self.btn_filter_points.configure(state='disabled')

    def enable(self):
        self.btn_visualize.configure(state='normal')
        self.btn_filter_points.configure(state='normal')


class SaveFrame(ctk.CTkFrame):
    def __init__(self, parent, parents_parent, las_manager):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.btn_save = BtnSave(self, las_manager.write_las, parents_parent.file_path)
        self.btn_save_as = BtnSaveAs(self, las_manager.write_las)

    def disable(self):
        self.btn_save.configure(state='disabled')
        self.btn_save_as.configure(state='disabled')

    def enable(self):
        self.btn_save.configure(state='normal')
        self.btn_save_as.configure(state='normal')
