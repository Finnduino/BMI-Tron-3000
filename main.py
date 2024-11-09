from ursina import *
from ursina.shaders import lit_with_shadows_shader

from scenes.entry_scene import EntryScene
from scenes.visualizer import VisualizerScene
app = Ursina()

entry_scene = EntryScene(dev=True)
visualizer_scene = VisualizerScene()

def switch_to_visualizer():
    entry_scene.disable()
    visualizer_scene.enable()

def switch_to_entry():
    visualizer_scene.disable()
    entry_scene.enable()
    

def build_house(name: str):
    #TODO: implement this
    print("brrr emulating talking to a server and serving the pdfs or whatever")
    visualizer_scene.load_building(name)
    
def found_model(cabin : str, shaft: str):
    print("Found model", cabin, shaft)
    visualizer_scene.load_elevator(cabin, shaft)


# Subscription to events
entry_scene.subscribe_to_move_to_visualizer(switch_to_visualizer)
entry_scene.subscribe_to_elevator(found_model)
entry_scene.subscribe_to_build_building(build_house)

entry_scene.scene.enabled = True
app.run()
