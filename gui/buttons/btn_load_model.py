import threading
import customtkinter as ctk
from tkinter import filedialog


# ideal button, all buttons should have this structure with minimal differences
class BtnLoadModel(ctk.CTkButton):
    def __init__(self, parent, func, disable_func, enable_func):
        super().__init__(master=parent, command=self.start_func_thread, text="wybierz model")
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.func = func
        self.pack(fill='x', pady=4, ipady=8)

    def start_func_thread(self):
        file_path = filedialog.askopenfilename(filetypes=[("joblib files", ["*.joblib"]),
                                                          ("compressed files",
                                                           ["*.z", "*.gz", "*.bz2", "*.xz", "*.lzma"]),
                                                          ("All files", "*.*")])
        # Wywołanie funkcji disable_func przed uruchomieniem wątku
        if file_path:
            self.disable_func()
            # Uruchomienie wątku z funkcją func
            threading.Thread(target=self.run_thread, args=(file_path,)).start()

    def run_thread(self, file_path):
        self.func(file_path)
        self.enable_func()
