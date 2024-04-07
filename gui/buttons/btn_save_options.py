import threading
import customtkinter as ctk


# ideal button, all buttons should have this structure with minimal differences
class BtnSaveOptions(ctk.CTkButton):
    def __init__(self, parent, func):
        super().__init__(master=parent, command=self.start_func_thread, text="Zapisz opcje")
        self.func = func
        self.pack(fill='x', pady=4, ipady=8, side='bottom')

    def start_func_thread(self):
        threading.Thread(target=self.run_thread).start()

    def run_thread(self):
        self.func()
