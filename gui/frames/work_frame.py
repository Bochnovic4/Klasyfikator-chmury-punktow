import customtkinter as ctk
import numpy as np

from gui.buttons.Separator import Separator
from gui.buttons.btn_top_generic import BtnGeneric
from gui.buttons.btn_train_model import BtnTrainModel
from gui.other_widgets.check_box_generic import CheckBoxGeneric


class WorkFrame(ctk.CTkFrame):
    def __init__(self, parent, gui_custom, las_manager, model):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.visualize_options = []
        self.check_box = []
        self.model = model

        self.btn_visualize = BtnGeneric(self, 'pokaż plik', gui_custom.visualize
                                        , gui_custom.disable_all, gui_custom.enable_all, side='bottom')
        self.btn_visualize_color = BtnGeneric(self, 'pokaż wybrane klasy', gui_custom.visualize_color,
                                              gui_custom.disable_all, gui_custom.enable_all,
                                              optional_argument=self.visualize_options, side='bottom')
        self.btn_filter_points = BtnGeneric(self, 'Usuń szum', las_manager.filter_points, gui_custom.disable_all,
                                            gui_custom.enable_all)
        self.btn_classify = BtnGeneric(self, 'Klasyfikuj punkty', model.classify,
                                       gui_custom.disable_all, gui_custom.enable_all, optional_argument=las_manager)
        self.btn_train_model = BtnTrainModel(self, model.train_model, las_manager,
                                             gui_custom.disable_all,
                                             gui_custom.enable_all)
        self.btn_visualize_color.configure(state="disabled")
        self.btn_classify.configure(state="disabled")

        Separator(self, "wybierz klasy do wyświetlenia")

        for x in np.unique(las_manager.classes):
            self.check_box.append(CheckBoxGeneric(self, x, self.visualize_classes, x))

    def visualize_classes(self, las_class, value):
        if las_class in self.visualize_options:
            self.visualize_options.remove(las_class)
            if len(self.visualize_options) == 0:
                self.btn_visualize_color.configure(state="disabled")
        else:
            self.visualize_options.append(las_class)
            if len(self.visualize_options) > 0:
                self.btn_visualize_color.configure(state="normal")

    def disable(self):
        self.btn_visualize.configure(state='disabled')
        self.btn_visualize_color.configure(state='disabled')
        self.btn_filter_points.configure(state='disabled')
        self.btn_classify.configure(state='disabled')
        self.btn_train_model.configure(state='disabled')
        for x in self.check_box:
            x.configure(state='disabled')

    def enable(self):
        self.btn_visualize.configure(state='normal')
        self.btn_filter_points.configure(state='normal')
        self.btn_train_model.configure(state='normal')
        for x in self.check_box:
            x.configure(state='normal')
        if self.model.is_enabled:
            self.btn_classify.configure(state='normal')
        if len(self.visualize_options) > 0:
            self.btn_visualize_color.configure(state='normal')
