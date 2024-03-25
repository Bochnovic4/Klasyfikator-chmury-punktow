import threading
import customtkinter as ctk
from tkinter import messagebox


# ideal button, all buttons should have this structure with minimal differences
class BtnTrainModel(ctk.CTkButton):
    def __init__(self, parent, func, points, classes, disable_func, enable_func):
        super().__init__(master=parent, command=self.show_confirmation_dialog, text="trenuj model")
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.points = points
        self.classes = classes
        self.func = func
        self.pack(fill='x', pady=4, ipady=8)

    def show_confirmation_dialog(self):
        result = messagebox.askquestion("Potwierdzenie", "Czy jesteś pewien? Może to zająć dużo czasu")
        if result == 'yes':
            self.start_func_thread()

    def start_func_thread(self):
        self.disable_func()

        threading.Thread(target=self.run_thread).start()

    def run_thread(self):
        self.func(self.points, self.classes)
        self.enable_func()
