from ursina import *
import scenes.scene_object
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser import FileButton

KONE_BLUE = color.hex("#1450F5")
BLACK = color.hex("#141414")
SAND = color.hex("#F3EEE6")
YELLOW = color.hex("#FFE141")
LIGHT_BLUE = color.hex("#D2F5FF")
PINK = color.hex("#FFCDD7")
WHITE = color.hex("#FFFFFF")


class EntryScene(scenes.scene_object.SceneObject):
    def __init__(self):
        super().__init__()
        self.scene = Entity()
        self.scene.enabled = False

        self.ui = Entity(
            parent=camera.ui,
        )

        self.autofill_title = Text("Submit all of the inputs at the same time", position=(0, 0.3), origin=(0, 0))
        
        self.select_button = Button(text='Browse File', color=KONE_BLUE, y=0.2, origin=(0, 0))
        self.select_button.fit_to_text()
        self.select_button.tooltip = Tooltip('Select the input folder to submit all of the inputs at the same time')
        self.select_button.on_click = self.select_model


        self.title = Text("Or submit the files Individually", position=(0, 0.1), origin=(0, 0))
        
        # Add the elevator model dropdown menu
        self.elevator_text = Text("Elevator Model", x=-0.3, y=-0.02, origin=(0, 0))
        self.elevator_select_menu = DropdownMenu("Select", buttons=(
            DropdownMenuButton("Model 1"),
            DropdownMenuButton("Model 2"),
        ), x=-0.3, y=-0.06, origin=(0, 0))

        # Add the shaft model dropdown menu
        self.shaft_text = Text("Shaft Model", position=(0.3, -0.02), origin=(0, 0))
        self.shaft_select_menu = DropdownMenu("Select", buttons=(
            DropdownMenuButton("Model 1"),
            DropdownMenuButton("Model 2"),
        ), position=(0.3, -0.06), origin=(0, 0))

        # Metadata file button
        self.metadata_text = Text("Metadata", x=-0.3, y=-0.2, origin=(0, 0))
        self.metadata_fb = Button(text='Browse File', color=KONE_BLUE, x=-0.3, y=-0.26, origin=(0, 0))
        self.metadata_fb.fit_to_text()

        # Floor plans file button
        self.floor_plans_text = Text("Floor Plans", x=0.3, y=-0.2, origin=(0, 0))
        self.floor_plans_fb = Button(text='Browse File', color=KONE_BLUE, x=0.3, y=-0.26, origin=(0, 0))
        self.floor_plans_fb.fit_to_text()

        # Add every entity to the scene
        self.autofill_title.parent = self.ui
        self.select_button.parent = self.ui
            self.title.parent = self.ui
        self.elevator_text.parent = self.ui
        self.elevator_select_menu.parent = self.ui
        self.shaft_text.parent = self.ui
        self.shaft_select_menu.parent = self.ui
        self.metadata_text.parent = self.ui
        self.metadata_fb.parent = self.ui
        self.floor_plans_text.parent = self.ui
        self.floor_plans_fb.parent = self.ui
    
    def select_button_macro(self):
        self.select_model()
        self.move_to_visualizer()
    
    def subscribe_to_elevator(self, methodname):
        """Subscribe to the found elevator event"""
        self.found_elevator_callback = methodname
    
    def subscribe_to_move_to_visualizer(self, methodname):
        """Subscribe to the open visualizer event"""
        self.move_to_visualizer = methodname
    
    def select_model(self, cabin: str = "elevator.gltf", shaft : str = "shaft.gltf"):
        """This method is called for selecting the elevator model"""        
        #Find the subdirectory where the 3D models are stored 
        self.found_elevator_callback(cabin, shaft)
        if os.path.exists(f"\\models\\{cabin}") and os.path.exists(f"\\models\\{shaft}"):
            path = "\\models\\"
            self.found_elevator_callback(path+cabin, path+shaft)
        # Here you can add the logic to select and load a 3D model
        
    def select_floor(self):
        """This method is called for each floor selected"""