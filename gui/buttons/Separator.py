import customtkinter as ctk
from settings import WHITE, BACKGROUND_COLOR


class Separator(ctk.CTkButton):
    def __init__(self, parent, text):
        super().__init__(master=parent, state='disabled', text_color_disabled=WHITE, fg_color=BACKGROUND_COLOR,
                         text=text)
        self.pack(fill='x', pady=4, ipady=8)
