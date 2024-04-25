import customtkinter as ctk

from gui.frames.option_frame import OptionFrame
from gui.frames.save_frame import SaveFrame
from gui.frames.work_frame import WorkFrame


class Menu(ctk.CTkTabview):
    def __init__(self, parent, las_manager, model):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        # tabs
        self.add('Działaj')
        self.add('Zapisz')
        self.add('Opcje')

        # widgets
        self.work_frame = WorkFrame(self.tab('Działaj'), parent, las_manager, model)
        self.save_frame = SaveFrame(self.tab('Zapisz'), parent, las_manager, model)
        self.option_frame = OptionFrame(self.tab("Opcje"), parent)

    def disable(self):
        self.work_frame.disable()
        self.save_frame.disable()

    def enable(self):
        self.work_frame.enable()
        self.save_frame.enable()
