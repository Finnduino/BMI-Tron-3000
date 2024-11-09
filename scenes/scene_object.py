from ursina import Entity

class SceneObject():
    """A class that represents a scene object"""
    def __init__(self, this_scene: Entity = Entity()):
        self.scene = this_scene
