import tkinter as tk
import customtkinter as ctk


class IntegerEntry(ctk.CTkEntry):
    def __init__(self, master=None, text_changed_callback=None, **kwargs):
        self.text_changed_callback = text_changed_callback
        self.var = tk.StringVar(master)
        validate_cmd = master.register(self.validate_input)
        kwargs["validate"] = "key"
        kwargs["validatecommand"] = (validate_cmd, "%P")
        super().__init__(master, textvariable=self.var, **kwargs)
        self.pack(padx=10, pady=10)
        if self.text_changed_callback:
            self.var.trace_add("write", self.on_text_changed)

    def validate_input(self, new_value):
        if new_value == "":
            return True
        if new_value.isdigit():
            if 0 <= int(new_value) <= 100:
                return True
        self.bell()
        return False

    def on_text_changed(self, *args):
        if self.text_changed_callback:
            self.text_changed_callback(self.get(), "MAX_DEPTH")
            print(self.get())
