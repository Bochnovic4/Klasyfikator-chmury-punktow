import customtkinter as ctk
from btn_open import *
from las_file_manager import LasFileManager


class Menu(ctk.CTkTabview):
    def __init__(self, parent, las_manager):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        # tabs
        self.add('temp1')
        self.add('temp2')

        # widgets
        TempFrame(self.tab('temp1'), las_manager)
        TempFrame2(self.tab('temp2'), las_manager)


class TempFrame(ctk.CTkFrame):
    def __init__(self, parent, las_manager):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        BtnVisualize(self, las_manager)


class TempFrame2(ctk.CTkFrame):
    def __init__(self, parent, las_manager):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
