import customtkinter

import customtkinter as ctk


class CheckBoxGeneric(ctk.CTkCheckBox):
    def __init__(self, parent, text, func, option_value, value=0):
        self.check_var = customtkinter.IntVar(value=value)
        super().__init__(master=parent, text=text, variable=self.check_var, onvalue=1, offvalue=0, command=self.check)
        self.func = func
        self.option_value = option_value
        self.pack(fill='x', pady=4, ipady=8, )

    def check(self):
        self.func(self.option_value, self.check_var.get())
