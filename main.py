from ursina import *
from ursina.shaders import lit_with_shadows_shader

from scenes.entry_scene import EntryScene
from scenes.visualizer import VisualizerScene
app = Ursina()

entry_scene = EntryScene()
visualizer_scene = VisualizerScene()

def switch_to_visualizer():
    entry_scene.disable()
    visualizer_scene.enable()

def switch_to_entry():
    visualizer_scene.disable()
    entry_scene.enable()


def found_model(cabin : str, shaft: str):
    print("FOUND ELEVATOR")
    visualizer_scene.load_elevator(cabin, shaft)


# Subscription to events
entry_scene.subscribe_to_move_to_visualizer(switch_to_visualizer)
entry_scene.subscribe_to_elevator(found_model)


entry_scene.scene.enabled = True
app.run()
