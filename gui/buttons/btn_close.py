import threading
import customtkinter as ctk
from tkinter import filedialog


class BtnClose(ctk.CTkButton):
    def __init__(self, parent, func,disable_func, enable_func):
        super().__init__(master=parent, command=self.start_func_thread, text="zmień plik las")
        self.func = func
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.pack(fill='x', pady=4, ipady=8)

    def start_func_thread(self):
        file_path = filedialog.askopenfilename(filetypes=[("Las Files", "*.las")])

        if file_path:
            self.disable_func()
            # Uruchomienie wątku z funkcją func
            threading.Thread(target=self.open_dialog, args=(file_path,)).start()

    def open_dialog(self, file_path):
        self.func(file_path)
        self.enable_func()
