from ursina import *
import scenes.scene_object
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser import FileButton
from ursina.prefabs.input_field import InputField
import tkinter as tk
from tkinter import filedialog


class ManualEditor(scenes.scene_object.SceneObject):
    def __init__(self):
        super().__init__()
        self.initial_setup = Entity(parent=self.ui, origin=(0, 0), position=(0, 0))
        self.autofill_title = Text("Select the base drawing", position=(0, 0.3), origin=(0, 0))
        self.autofill_title.parent = self.initial_setup
        self.select_button = Button(text='Browse File', color=color.azure, y=0.2, origin=(0, 0))
        self.select_button.fit_to_text()
        self.select_button.tooltip = Tooltip('Select the base drawing to start editing')
        self.select_button.on_click = self.open_png_dialog
        self.select_button.parent = self.initial_setup
        
        
    def open_png_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(file_path)
        