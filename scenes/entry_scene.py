from ursina import *
import scenes.scene_object

class EntryScene(scenes.scene_object.SceneObject):
    def __init__(self):
        super().__init__()
        self.scene = Entity()
        
        
        self.select_button = Button(text='Select Demo World', color=color.azure, scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.4)
        self.found_elevator_callback = None
        self.move_to_visualizer = None
        self.select_button.tooltip = Tooltip('Select a 3D model to use')
        self.select_button.on_click = self.select_button_macro
        self.scene.enabled = False
        self.select_button.parent = self.ui
        
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