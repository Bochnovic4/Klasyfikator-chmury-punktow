import customtkinter as ctk
import settings
from gui.buttons.Separator import Separator
from gui.buttons.btn_save_options import BtnSaveOptions
from gui.other_widgets.combobox_n_jobs_option import NJobsOption


class OptionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.options = settings
        Separator(self, "ilość wykorzystywanych rdzeni do traningu modelu:")
        self.n_jobs_option = NJobsOption(self, self.set_options_temporary)
        self.btn_save_options = BtnSaveOptions(self, self.update_settings)

    def set_options_temporary(self, value, option):
        setattr(self.options, option, value)

    def update_settings(self):
        with open("D:\\szkoła\\semestr 6\\Projekt Zespołowy\\Klasyfikator-chmury-punktow\\settings.py", "w") as file:
            file.write("# colors\n")
            file.write(f"BACKGROUND_COLOR = \"{self.options.BACKGROUND_COLOR}\"\n")
            file.write(f"WHITE = \"{self.options.WHITE}\"\n")
            file.write(f"RED = \"{self.options.RED}\"\n\n")

            file.write("# visualization colors\n")
            file.write("LABEL_COLORS = {\n")
            for key, value in self.options.LABEL_COLORS.items():
                file.write(f"    {key}: {value},\n")
            file.write("}\n\n")

            file.write("# Liczba rdzeni do traningu modelu\n")
            file.write(f"N_JOBS = {self.options.N_JOBS}\n\n")

            file.write("# kolumny do treningu modelu\n")
            file.write(f"COLUMNS = {self.options.COLUMNS}\n")
