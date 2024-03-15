import customtkinter as ctk
from tkinter import filedialog
from settings import *
from las_file_manager import LasFileManager

# wybierz plik
class BtnOpen(ctk.CTkFrame):

    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.import_func = import_func

        ctk.CTkButton(self, text='wybierz plik', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Las Files", "*.las")])
        self.import_func(path)


# zamknij plik(zmień go bez wychodzenia z aplikacji)
class BtnClose(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent, command=close_func, text='x', text_color=WHITE,
                         fg_color='transparent', width=40, height=40, corner_radius=0, hover_color=RED)
        self.place(relx=0.99, rely=0.01, anchor='ne')


class BtnVisualize(ctk.CTkButton):
    def __init__(self, parent, las_manager):
        super().__init__(master=parent, command=self.visualize, text='pokaż plik')
        self.las_manager = las_manager
        self.pack(fill='x', pady=4, ipady=8, side='bottom')

    def visualize(self):
        self.las_manager.visualize()

