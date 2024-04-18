import customtkinter as ctk


class BtnVisualizeColor(ctk.CTkButton):
    def __init__(self, parent, func,visualize_classes ,disable_func):
        super().__init__(master=parent, command=self.visualize, text='pokaż plik klasy')
        self.disable_func = disable_func
        self.visualize_classes = visualize_classes
        self.func = func
        self.pack(fill='x', pady=4, ipady=8, side='bottom')

    def visualize(self):
        self.disable_func()
        self.func(self.visualize_classes)
