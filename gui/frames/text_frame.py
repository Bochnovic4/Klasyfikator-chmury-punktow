import customtkinter as ctk


class TextFrame(ctk.CTkFrame):
    def __init__(self, parent, dane):
        super().__init__(master=parent)
        self.grid(column=1, row=0, sticky='nsew', padx=50, pady=25)

        self.labels = {}

        self.bind("<Configure>", self.update_wraplength)

        # Tworzenie etykiet na podstawie danych
        for key, var in dane.items():
            label = ctk.CTkLabel(self, text=f"{key}: {var}")
            label.grid(row=len(self.labels), column=0, sticky='w')
            self.labels[key] = label

    # wrap length of text is dynamic
    def update_wraplength(self, event=None):
        for label in self.labels.values():
            container_width = self.winfo_width() - self.grid_info()['padx'] * 2
            wrap_length = int(container_width * 0.9)  # use 90% of available space in container
            label.update_idletasks()
            label.configure(wraplength=wrap_length)

    def update_data(self, new_data):
        for key, value in new_data.items():
            if key in self.labels:
                self.labels[key].configure(text=f"{key}: {value}")
