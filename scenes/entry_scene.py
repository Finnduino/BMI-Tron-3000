import json
from re import match

from ursina import *
import scenes.scene_object
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser import FileButton
from ursina.prefabs.input_field import InputField
import tkinter as tk
from tkinter import filedialog


KONE_BLUE = color.hex("#1450F5")
BLACK = color.hex("#141414")
SAND = color.hex("#F3EEE6")
YELLOW = color.hex("#FFE141")
LIGHT_BLUE = color.hex("#D2F5FF")
PINK = color.hex("#FFCDD7")
WHITE = color.hex("#FFFFFF")


class EntryScene(scenes.scene_object.SceneObject):
    def __init__(self, dev=False):
        super().__init__()
        self.dev = dev
        self.scene = Entity()
        self.scene.enabled = False

        self.ui = Entity(
            parent=camera.ui,
        )

        #Subscription variables
        self.found_elevator_callback = None
        self.move_to_visualizer_callback = None
        self.build_building_callback = None
        self.move_to_manual_editor_callback = None
        
        self.autofill_title = Text("Submit all of the inputs at the same time", position=(0, 0.3), origin=(0, 0))

        self.files_selected=0
        
        self.select_button = Button(text='Browse File', color=KONE_BLUE, y=0.2, origin=(0, 0))
        self.select_button.fit_to_text()
        self.select_button.tooltip = Tooltip('Select the input folder to submit all of the inputs at the same time')
        self.select_button.on_click = self.open_pdf_dialog



        self.load_save_button = Button(text='Load Save File', color=color.azure, scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.3)
        self.load_save_button.fit_to_text()
        self.load_save_button.tooltip = Tooltip('Load a saved state')
        self.load_save_button.on_click = self.load_save_file
        self.load_save_button.parent = self.ui

        self.title = Text("Or submit the files Individually", position=(0, 0.1), origin=(0, 0))
        
        # Add the elevator model dropdown menu
        self.elevator_text = Text("Elevator Model", origin=(0, -1))
        self.elevator_success = Text("Successfully loaded", origin=(0, -1), position=(0.1, 0))
        self.elevator_success.enabled = False
        self.elevator_select_menu = DropdownMenu("Select", buttons=(
            DropdownMenuButton("Model 1", on_click=lambda:self.select_model("One", "One")),
            DropdownMenuButton("Model 2", on_click=lambda: self.select_model("Two", "Two")),
            DropdownMenuButton("Model 3", on_click=lambda: self.select_model("Three", "Three")),
        ), x=-0.115, y=0)

        self.eleveator_wrapper = Entity(parent=self.ui, origin=(0,0), position=(-0.3, -0.06))
        self.elevator_text.parent = self.eleveator_wrapper
        self.elevator_success.parent = self.eleveator_wrapper
        self.elevator_select_menu.parent = self.eleveator_wrapper
        #contains the paths of the selected files
        self.seleceted_files=[]

        # Add the shaft model dropdown menu
        self.shaft_text = Text("Scale", origin=(0 , -1), position=(0,0))
        self.scale_input = InputField(limit_content_to='0123456789:', active=True, position=(0, -0.02))
        
        self.shaft_wrapper = Entity(parent=self.ui, origin=(0,0), position=(0.3, -0.06))
        self.shaft_text.parent = self.shaft_wrapper
        self.scale_input.parent = self.shaft_wrapper

        # Metadata file button
        self.metadata_text = Text("Manual Editor", x=-0.3, y=-0.2, origin=(0, 0))
        self.metadata_fb = Button(text='Manually map the layout', color=KONE_BLUE, x=-0.3, y=-0.26, origin=(0, 0))
        self.metadata_fb.fit_to_text()
        self.metadata_fb.on_click = lambda: self.move_to_manual_editor_callback()

        # Floor plans file button
        self.floor_plans_text = Text("Floor Plans", x=0.3, y=-0.2, origin=(0, 0))
        self.floor_plans_fb = Button(text='Browse File', color=KONE_BLUE, x=0.3, y=-0.26, origin=(0, 0))
        self.floor_plans_fb.fit_to_text()

        # Add every entity to the scene
        self.autofill_title.parent = self.ui
        self.select_button.parent = self.ui
        self.title.parent = self.ui
        self.metadata_text.parent = self.ui
        self.metadata_fb.parent = self.ui
        self.floor_plans_text.parent = self.ui
        self.floor_plans_fb.parent = self.ui
    
        self.load_button = Button(text='Load world', color=color.azure, scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.4)
        self.load_button.fit_to_text()
        self.load_button.parent = self.ui
    
        self.load_button.tooltip = Tooltip('Load world')
        self.load_button.on_click = self.select_button_macro


        self.elevator_val = 1 #default value


        if self.dev:
            self.default_load = Button(text='Load default', color=color.azure, scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.2)
            self.default_load.fit_to_text()
            self.default_load.parent = self.ui
            self.default_load.tooltip = Tooltip('Load default')
            self.default_load.on_click = lambda: self.build_building_callback("Default", self.elevator_val)



    
    def select_button_macro(self):
        self.move_to_visualizer_callback()
    
    def subscribe_to_elevator(self, methodname):
        """Subscribe to the found elevator event"""
        self.found_elevator_callback = methodname
    
    def subscribe_to_move_to_visualizer(self, methodname):
        """Subscribe to the open visualizer event"""
        self.move_to_visualizer_callback = methodname
    
    def subscribe_to_build_building(self, methodname):
        """Subscribe to the build building event"""
        print("Subscribed to build building")
        self.build_building_callback = methodname
    
    def subscribe_to_open_manual_editor(self, methodname):
        self.move_to_manual_editor_callback = methodname



    def select_model(self, cabin: str = "elevatorOne", shaft : str = "shaftOne"):
        """This method is called for selecting the elevator model"""        
        #Find the subdirectory where the 3D models are stored
        if cabin == "One": self.elevator_val = 1
        elif cabin == "Two": self.elevator_val = 2
        elif cabin == "Three": self.elevator_val = 3

        self.found_elevator_callback(cabin, shaft)
        #if os.path.exists(f"\\models\\{cabin}") and os.path.exists(f"\\models\\{shaft}"):
        #    path = "\\models\\"
        #    self.found_elevator_callback(path+cabin, path+shaft)
        # Here you can add the logic to select and load a 3D model

    
    def select_building(self):
        """This method is called for selecting the building model"""
        # Here you can add the logic to select and load a building model
        for each in self.seleceted_files:
            self.build_building_callback
    
    def select_floor(self):
        """This method is called for each floor selected"""

    def load_save_file(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.apply_loaded_data(data)

    def apply_loaded_data(self, data):
        # Example implementation to apply loaded data
        input_files = data.get('input_files', [])
        elevator_position = data.get('elevator_position', None)

        for file_path in input_files:
            self.build_building_callback(file_path, self.elevator_val)

        if elevator_position:
            print("Elevator position should be changed ?")

        
    def open_pdf_dialog(self):
        """Open a file dialog to select multiple PDF files"""
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf"),("OBJ files", "*.obj"),("Image files", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            self.files_selected = self.files_selected+1

            self.select_button.text=f"Browse File ({self.files_selected} files selected)"
            self.select_button.fit_to_text()
            print("Selected files:", file_paths)
            for each in file_paths:
                self.build_building_callback(each,self.elevator_val)
            # Handle the selected files here

        #TODO Integrate with our backend
        #For now, it calls with the default values, resulting in the default building
        #self.build_building_callback("Default")
        
