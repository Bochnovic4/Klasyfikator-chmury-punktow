import customtkinter as ctk
import tkinter as tk
import os

from settings import N_JOBS


class NJobsOption(ctk.CTkOptionMenu):
    def __init__(self, parent, func):
        num_cores = os.cpu_count()
        values = [str(i) for i in range(1, num_cores + 1)]
        self.variable = tk.StringVar(parent, value=str(N_JOBS))
        super().__init__(master=parent, values=values, command=self.on_select)
        self.func = func
        self.number = N_JOBS
        if self.number == -1:
            self.number = num_cores
        self.set(self.number)
        self.pack(fill='x', pady=4, ipady=8)

    def on_select(self, choice):
        self.func(choice, "N_JOBS")
