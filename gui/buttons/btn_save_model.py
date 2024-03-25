import threading
import customtkinter as ctk
from tkinter import filedialog


class BtnSaveModel(ctk.CTkButton):
    def __init__(self, parent, func, disable_func, enable_func):
        super().__init__(master=parent, command=self.start_func_thread, text="zapisz model", state='disabled')
        self.disable_func = disable_func
        self.enable_func = enable_func
        self.func = func
        self.pack(fill='x', pady=4, ipady=8)

    def start_func_thread(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".joblib", filetypes=[("joblib files", "*.joblib"), ("All files", "*.*")])
        # Wywołanie funkcji disable_func przed uruchomieniem wątku
        self.disable_func()
        # Uruchomienie wątku z funkcją func
        threading.Thread(target=self.run_thread, args=(file_path,)).start()

    def run_thread(self, file_path):
        # Wywołanie funkcji func z przekazanym argumentem file_path
        self.func(file_path)
        # Wywołanie funkcji enable_func po zakończeniu wątku
        self.enable_func()
