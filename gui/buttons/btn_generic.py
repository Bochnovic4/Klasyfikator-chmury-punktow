import threading
import customtkinter as ctk


# generic button creator if function to use doesn't have input variables you can use this
class BtnCreator(ctk.CTkButton):
    def __init__(self, parent, text, func_import, disable_func, enable_func):
        super().__init__(master=parent, command=self.start_func_thread, text=text)
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.func_import = func_import
        self.pack(fill='x', pady=4, ipady=8)

    def start_func_thread(self):
        self.disable_func()
        threading.Thread(target=self.func,).start()

    def func(self):
        self.func_import()
        self.enable_func()
