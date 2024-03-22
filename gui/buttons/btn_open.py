import threading
import customtkinter as ctk
from tkinter import filedialog


# choose file, using new thread
class BtnOpen(ctk.CTkFrame):

    def __init__(self, parent, func):
        super().__init__(master=parent)
        self.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.func = func

        self.button = ctk.CTkButton(self, text='wybierz plik', command=self.start_func_thread).pack(expand=True)

    def start_func_thread(self):
        file_path = filedialog.askopenfilename(filetypes=[("Las Files", "*.las")])

        if file_path:
            # Uruchomienie wątku z funkcją func
            threading.Thread(target=self.open_dialog, args=(file_path,)).start()

    def open_dialog(self, file_path):
        self.func(file_path)
