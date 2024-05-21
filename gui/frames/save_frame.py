import customtkinter as ctk
from gui.buttons.Separator import Separator
from gui.buttons.btn_close import BtnClose
from gui.buttons.btn_load_model import BtnLoadModel
from gui.buttons.btn_save_model import BtnSaveModel
from gui.buttons.btn_generic import BtnGeneric
from gui.buttons.bts_save_as import BtnSaveAs


class SaveFrame(ctk.CTkFrame):
    def __init__(self, parent, gui_custom, las_manager, model):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.model = model

        self.btn_save = BtnGeneric(self, 'Zapisz', las_manager.write_las,
                                   gui_custom.disable_all, gui_custom.enable_all,
                                   optional_argument=gui_custom.file_path)
        self.btn_save_as = BtnSaveAs(self, las_manager.write_las)

        self.btn_close = BtnClose(self, gui_custom.choose_file, gui_custom.disable_all,
                                  gui_custom.enable_all)

        Separator(self, "Model:")

        self.btn_load_model = BtnLoadModel(self, model.load, gui_custom.disable_all,
                                           gui_custom.enable_all)
        self.btn_save_model = BtnSaveModel(self, model.save, gui_custom.disable_all,
                                           gui_custom.enable_all)

    def disable(self):
        self.btn_save.configure(state='disabled')
        self.btn_save_as.configure(state='disabled')
        self.btn_load_model.configure(state='disabled')
        self.btn_save_model.configure(state='disabled')
        self.btn_close.configure(state='disabled')

    def enable(self):
        self.btn_save.configure(state='normal')
        self.btn_save_as.configure(state='normal')
        self.btn_load_model.configure(state='normal')
        self.btn_close.configure(state='normal')
        if self.model.is_enabled:
            self.btn_save_model.configure(state='normal')
