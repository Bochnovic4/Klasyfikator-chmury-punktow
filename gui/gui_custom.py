import numpy as np
import laspy
import customtkinter as ctk
from PIL import Image, ImageTk
import open3d as o3d

from gui.btn_open import BtnOpen
from settings import *


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.points = None
        self.file_path = None
        self.visualization = None
        self.canvas_widget = None
        self.canvas_frame = None
        ctk.set_appearance_mode('dark')

        # otwieraj jako zmaksymalizowane okno
        self.after(0, lambda: self.wm_state('zoomed'))
        self.title('temp')

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # widgets
        self.btn_open = BtnOpen(self, self.choose_file)

        # robienie canvasu
        # nie mam pojęcia jak to przenieść do osobnej funkcji by działało
        self.points_added = False

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_widget = ctk.CTkCanvas(self.canvas_frame, bg=BACKGROUND_COLOR, border=0, highlightthickness=0)

        self.canvas_frame.grid(row=0, column=0)

        self.canvas_widget.pack(fill="both", expand=True)

        self.last_x = None
        self.last_y = None
        self.scale_factor = 1.0

        self.mainloop()

    def choose_file(self, path):
        if path:
            self.btn_open.grid_forget()
            self.file_path = path
            self.load_lidar_data()

    def load_lidar_data(self):
        self.canvas_widget.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas_widget.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas_widget.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas_widget.bind("<MouseWheel>", self.on_mouse_scroll)

        self.canvas_frame.grid_configure(row=0, column=1, sticky="nsew")

        self.visualization = o3d.visualization.Visualizer()
        self.visualization.create_window(visible=False)  # Ustawienie visible na False

        las_file = laspy.read(self.file_path)

        xyz = np.vstack((las_file.x, las_file.y, las_file.z)).T
        colors = np.vstack((las_file.red, las_file.green, las_file.blue)).T / 65535.0

        points = o3d.geometry.PointCloud()
        points.points = o3d.utility.Vector3dVector(xyz)

        if colors.shape[0] == xyz.shape[0]:
            points.colors = o3d.utility.Vector3dVector(colors)

        # Obliczanie przesunięcia, aby środek chmury punktów był na środku Canvas
        canvas_center = np.array([self.canvas_widget.winfo_width() / 2, self.canvas_widget.winfo_height() / 2, 0])
        points_center = np.mean(xyz, axis=0)
        translation = canvas_center - points_center
        points.translate(translation)

        # Skalowanie punktów do rozmiaru canvasu
        scale_factor = min(self.canvas_widget.winfo_width(), self.canvas_widget.winfo_height()) / max(
            xyz[:, :2].max(axis=0) - xyz[:, :2].min(axis=0))
        points.scale(scale_factor, center=points_center)

        self.points = points
        self.points_added = False

        self.update_view()

    def update_view(self):
        if not self.points_added:
            self.visualization.add_geometry(self.points)
            self.points_added = True
        else:
            self.visualization.update_geometry(self.points)

        self.visualization.poll_events()
        self.visualization.update_renderer()

        img = self.visualization.capture_screen_float_buffer()
        img = (np.asarray(img) * 255).astype(np.uint8)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        self.canvas_widget.create_image(0, 0, anchor="nw", image=img)
        self.canvas_widget.image = img

    def on_mouse_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_mouse_drag(self, event):
        if self.last_x is not None and self.last_y is not None:
            dx = event.x - self.last_x
            dy = event.y - self.last_y

            self.visualization.get_view_control().rotate(dx, dy)

            self.last_x = event.x
            self.last_y = event.y

            self.update_view()

    def on_mouse_release(self, event):
        self.last_x = None
        self.last_y = None

    def on_mouse_scroll(self, event):
        # Określenie kierunku przewijania
        if event.delta > 0:
            scale_factor = SZYBKOSC_SCROLLOWANIA_OBRAZU  # Przybliżanie
        elif event.delta < 0:
            scale_factor = -SZYBKOSC_SCROLLOWANIA_OBRAZU  # Oddalanio
        else:
            return  # Nie zmieniaj skali, jeśli delta wynosi zero

        # Skalowanie widoku
        self.scale_factor *= scale_factor
        self.visualization.get_view_control().scale(scale_factor)
        self.update_view()
