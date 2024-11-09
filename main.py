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

entry_scene.scene.enabled = True
entry_scene.set_select_button(switch_to_visualizer)
app.run()
