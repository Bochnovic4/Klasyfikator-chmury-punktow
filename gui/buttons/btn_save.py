import customtkinter as ctk


class BtnSave(ctk.CTkButton):
    def __init__(self, parent, func, path):
        super().__init__(master=parent, command=self.func, text="zapisz")
        self.func = func
        self.file_path = path
        self.pack(fill='x', pady=4, ipady=8)

    def func(self):
        self.func(self.file_path)
