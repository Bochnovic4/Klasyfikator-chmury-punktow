import threading
import customtkinter as ctk


class BtnClassify(ctk.CTkButton):
    def __init__(self, parent, func_import, points, disable_func, enable_func):
        super().__init__(master=parent, command=self.start_func_thread, text="Klasyfikuj punkty", state='disabled')
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.func_import = func_import
        self.points = points
        self.pack(fill='x', pady=4, ipady=8)

    def start_func_thread(self):
        self.disable_func()
        threading.Thread(target=self.func, ).start()

    def func(self):
        self.func_import(self.points)
        self.enable_func()
