import customtkinter as ctk
from tkinter import filedialog


class BtnSaveAs(ctk.CTkButton):
    def __init__(self, parent, func):
        super().__init__(master=parent, command=self.func, text="zapisz jako")
        self.func = func
        self.pack(fill='x', pady=4, ipady=8)

    def func(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".las",
                                                 filetypes=[("LAS files", "*.las"), ("All files", "*.*")])
        self.func(file_path)
