import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from settings import *
from las_file_manager import LasFileManager


# choose file
class BtnOpen(ctk.CTkFrame):

    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.import_func = import_func

        ctk.CTkButton(self, text='wybierz plik', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Las Files", "*.las")])
        self.import_func(path)


# close file(without closing application)
class BtnClose(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent, command=close_func, text='x', text_color=WHITE,
                         fg_color='transparent', width=40, height=40, corner_radius=0, hover_color=RED)
        self.place(relx=0.99, rely=0.01, anchor='ne')


class BtnVisualize(ctk.CTkButton):
    def __init__(self, parent, func, disable_func):
        super().__init__(master=parent, command=self.visualize, text='pokaż plik')
        self.disable_func = disable_func
        self.func = func
        self.pack(fill='x', pady=4, ipady=8, side='bottom')

    def visualize(self):
        self.disable_func()
        self.func()

# generic button creator if function to use doesn't have input variables you can use this
class BtnCreator(ctk.CTkButton):
    def __init__(self, parent, text, func, disable_func, enable_func):
        super().__init__(master=parent, command=self.func, text=text)
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.func = func
        self.pack(fill='x', pady=4, ipady=8)

    def func(self):
        self.disable_func()
        self.after(1, lambda: self.func())
        self.after(2, lambda: self.enable_func())


class BtnSave(ctk.CTkButton):
    def __init__(self, parent, func, path):
        super().__init__(master=parent, command=self.func, text="zapisz")
        self.func = func
        self.file_path = path
        self.pack(fill='x', pady=4, ipady=8)

    def func(self):
        self.func(self.file_path)


class BtnSaveAs(ctk.CTkButton):
    def __init__(self, parent, func):
        super().__init__(master=parent, command=self.func, text="zapisz jako")
        self.func = func
        self.pack(fill='x', pady=4, ipady=8)

    def func(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".las",
                                                 filetypes=[("LAS files", "*.las"), ("All files", "*.*")])
        self.func(file_path)


class Frame(ctk.CTkFrame):
    def __init__(self, parent, dane):
        super().__init__(master=parent)
        self.grid(column=1, row=0, sticky='nsew', padx=50, pady=25)

        self.labels = {}

        self.bind("<Configure>", self.update_wraplength)

        # Tworzenie etykiet na podstawie danych
        for key, var in dane.items():
            label = ctk.CTkLabel(self, text=f"{key}: {var}")
            label.grid(row=len(self.labels), column=0, sticky='w')
            self.labels[key] = label

    # wrap length of text is dynamic
    def update_wraplength(self, event=None):
        for label in self.labels.values():
            container_width = self.winfo_width() - self.grid_info()['padx']*2
            wrap_length = int(container_width * 0.9) # use 90% of available space in container
            label.update_idletasks()
            label.configure(wraplength=wrap_length)
    def update_data(self, new_data):
        for key, value in new_data.items():
            if key in self.labels:
                self.labels[key].configure(text=f"{key}: {value}")
