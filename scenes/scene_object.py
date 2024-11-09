from ursina import Entity
from ursina import camera
class SceneObject():
    """A class that represents a scene object"""
    
    def __init__(self):
        self.scene = Entity()
        self.ui = Entity(parent=camera.ui)
    def enable(self):
        """Enable the scene"""
        self.scene.enabled = True
        self.ui.enabled = True

    def disable(self):
        """Disable the scene"""
        self.scene.enabled = False
        self.ui.enabled = False