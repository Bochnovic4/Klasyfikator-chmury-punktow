import threading
import customtkinter as ctk


class BtnGeneric(ctk.CTkButton):
    def __init__(self, parent, text, func_import, disable_func, enable_func, optional_argument=None, side='top'):
        super().__init__(master=parent, command=self.start_func_thread, text=text)
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.func_import = func_import
        self.optional_argument = optional_argument
        self.pack(fill='x', pady=4, ipady=8, side=side)

    def start_func_thread(self):
        self.disable_func()
        threading.Thread(target=self.func).start()

    def func(self):
        if self.optional_argument is not None:
            self.func_import(self.optional_argument)
        else:
            self.func_import()
        self.enable_func()
