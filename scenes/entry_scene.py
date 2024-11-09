from ursina import *
import scenes.scene_object

class EntryScene(scenes.scene_object.SceneObject):
    def __init__(self):
        self.scene = Entity()
        self.ui = Entity(parent=camera.ui)

        self.select_button = Button(text='Select Model', color=color.azure)
        
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
    
    def select_model(self):
        print("Model selected")
        # Here you can add the logic to select and load a 3D mode