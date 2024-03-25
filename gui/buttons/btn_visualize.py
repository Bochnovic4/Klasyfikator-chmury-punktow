import customtkinter as ctk


class BtnVisualize(ctk.CTkButton):
    def __init__(self, parent, func, disable_func):
        super().__init__(master=parent, command=self.visualize, text='pokaż plik')
        self.disable_func = disable_func
        self.func = func
        self.pack(fill='x', pady=4, ipady=8, side='bottom')

    def visualize(self):
        self.disable_func()
        self.func()
