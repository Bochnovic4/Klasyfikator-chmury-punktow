import customtkinter as ctk
from tkinter import filedialog


class BtnOpen(ctk.CTkFrame):

    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.import_func = import_func

        ctk.CTkButton(self, text='wybierz plik', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Las Files", "*.las")])
        self.import_func(path)


