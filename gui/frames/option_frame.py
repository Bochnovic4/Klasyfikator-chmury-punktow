import customtkinter as ctk
import settings
from gui.buttons.Separator import Separator
from gui.buttons.btn_top_generic import BtnGeneric
from gui.other_widgets.entry_int import IntegerEntry
from gui.other_widgets.check_box_generic import CheckBoxGeneric
from gui.other_widgets.combobox_n_jobs_option import NJobsOption


class OptionFrame(ctk.CTkFrame):
    def __init__(self, parent, gui_custom):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.options = settings
        self.position_all = ['z', 'intensity', 'ball_density', 'cylinder_density', 'phi_angles_of_normal_vectors',
                             'theta_angles_of_normal_vectors', 'min_height', 'max_height', 'mean_height']

        Separator(self, "ilość wykorzystywanych rdzeni do traningu modelu:")
        self.n_jobs_option = NJobsOption(self, self.set_options_temporary)

        self.btn_save_options = BtnGeneric(self, 'Zapisz opcje', self.update_settings,
                                           gui_custom.disable_all, gui_custom.enable_all, side='bottom')

        Separator(self, "Maksymalna glebokosc drzewa:")
        self.depth = IntegerEntry(self, self.set_options_temporary)

        Separator(self, "kolumny do treningu modelu:")
        self.current_collumns = self.options.COLUMNS
        self.check_test = []

        for x in self.position_all:
            self.check_test.append(CheckBoxGeneric(self, x.replace("_", " "), self.set_checkbox_options,
                                                   x, 1 if x in self.current_collumns else 0))

    def set_checkbox_options(self, option_value, value):
        if value:
            self.current_collumns.append(option_value)
            self.current_collumns.sort(key=lambda x: self.position_all.index(x))
        else:
            self.current_collumns.remove(option_value)

        self.set_options_temporary(self.current_collumns, 'COLUMNS')

    def set_options_temporary(self, value, option):
        setattr(self.options, option, value)

    def update_settings(self):
        with open("settings.py", "w") as file:
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

            file.write("# Maksymalna glebokosc drzewa\n")
            file.write(f"MAX_DEPTH = {self.options.MAX_DEPTH}\n\n")

            file.write("# kolumny do treningu modelu\n")
            file.write(f"COLUMNS = {self.options.COLUMNS}\n")
