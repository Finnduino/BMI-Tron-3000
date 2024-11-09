from ursina import *
import scenes.scene_object

class EntryScene(scenes.scene_object.SceneObject):
    def __init__(self):
        self.scene = Entity()
        self.ui = Entity(parent=camera.ui)

        self.select_button = Button(text='Select Demo World', color=color.azure, scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.4)
        
        self.select_button.tooltip = Tooltip('Select a 3D model to use')
        self.select_button.on_click = self.select_model
        self.scene.enabled = False
        self.select_button.parent = self.ui
    
    def enable(self):
        self.scene.enabled = True
        self.ui.enabled = True
        
    def disable(self):
        self.scene.enabled = False
        self.ui.enabled = False
        
    def set_select_button(self, methodname):
        """Set the method to be called when the select button is clicked"""
        self.select_button.on_click = methodname
    
    def select_model(self, model_name: str = "default"):
        """This method is called for selecting the elevator model"""        
        #Find the subdirectory where the 3D models are stored 
        try: 
            model_path = "/models/" + model_name
            #Load the 3D model
            model = load_model(model_path)
            #Call the method to select the floor
            self.select_floor()
        except:
            print("Error loading model")
        # Here you can add the logic to select and load a 3D model
        
    def select_floor(self):
        """This method is called for each floor selected"""