import customtkinter as ctk
import settings
from gui.buttons.Separator import Separator
from gui.buttons.btn_save_options import BtnSaveOptions
from gui.frames.check_box_generic import CheckBoxGeneric
from gui.other_widgets.combobox_n_jobs_option import NJobsOption


class OptionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.options = settings
        Separator(self, "ilość wykorzystywanych rdzeni do traningu modelu:")
        self.n_jobs_option = NJobsOption(self, self.set_options_temporary)
        self.btn_save_options = BtnSaveOptions(self, self.update_settings)

        self.current_collumns = self.options.COLUMNS
        self.check_test = CheckBoxGeneric(self, "x", self.set_checkbox_options,
                                          'x', 1 if 'x' in self.current_collumns else 0)
        self.check_test = CheckBoxGeneric(self, "y", self.set_checkbox_options,
                                          'y', 1 if 'y' in self.current_collumns else 0)
        self.check_test = CheckBoxGeneric(self, "z", self.set_checkbox_options,
                                          'z', 1 if 'z' in self.current_collumns else 0)
        self.check_test = CheckBoxGeneric(self, "number of returns", self.set_checkbox_options,
                                          'number_of_returns', 1 if 'number_of_returns' in self.current_collumns else 0)
        self.check_test = CheckBoxGeneric(self, "intensity", self.set_checkbox_options,
                                          'intensity', 1 if 'intensity' in self.current_collumns else 0)

    def set_checkbox_options(self, option_value, value):
        position = ['x', 'y', 'z', 'number_of_returns', 'intensity']
        if value:
            self.current_collumns.append(option_value)
            self.current_collumns.sort(key=lambda x: position.index(x))
        else:
            self.current_collumns.remove(option_value)

        self.set_options_temporary(self.current_collumns,'COLUMNS')

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
