import customtkinter as ctk

from gui.buttons.btn_classify import BtnClassify
from gui.buttons.btn_generic import BtnCreator
from gui.buttons.btn_train_model import BtnTrainModel
from gui.buttons.btn_visualize import BtnVisualize


class WorkFrame(ctk.CTkFrame):
    def __init__(self, parent, gui_custom, las_manager, model):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.model = model

        self.btn_visualize = BtnVisualize(self, gui_custom.visualize, gui_custom.disable_all)
        self.btn_filter_points = BtnCreator(self, "Usuń szum", las_manager.filter_points, gui_custom.disable_all,
                                            gui_custom.enable_all)
        self.btn_classify = BtnClassify(self, model.classify, las_manager.points, gui_custom.disable_all,
                                        gui_custom.enable_all)
        self.btn_train_model = BtnTrainModel(self, model.train_model, las_manager.points, las_manager.classes,
                                             gui_custom.disable_all,
                                             gui_custom.enable_all)

    def disable(self):
        self.btn_visualize.configure(state='disabled')
        self.btn_filter_points.configure(state='disabled')
        self.btn_classify.configure(state='disabled')
        self.btn_train_model.configure(state='disabled')

    def enable(self):
        self.btn_visualize.configure(state='normal')
        self.btn_filter_points.configure(state='normal')
        self.btn_train_model.configure(state='normal')
        if self.model.model is not None:
            self.btn_classify.configure(state='normal')
