from ursina import *
from ursina.shaders import lit_with_shadows_shader

from scenes.entry_scene import EntryScene
from scenes.visualizer import VisualizerScene
from scenes.mapping_scene import ManualEditor
app = Ursina()
visualizer_scene= VisualizerScene()
entry_scene = EntryScene(dev=True)
manual_editor_scene = ManualEditor()

def switch_to_visualizer():
    entry_scene.disable()
    visualizer_scene.enable()
    manual_editor_scene.disable()
    visualizer_scene.camera = EditorCamera()
    visualizer_scene.camera.parent = visualizer_scene.scene

    
    
def switch_to_entry():
    visualizer_scene.disable()
    entry_scene.enable()
    manual_editor_scene.disable()

def switch_to_manual_editor():
    visualizer_scene.disable()
    entry_scene.disable()
    manual_editor_scene.enable()

def build_house(name: str, elevatorNbr):
    #TODO: implement this
    print("brrr emulating talking to a server and serving the pdfs or whatever")
    visualizer_scene.load_building(name,elevatorNbr)
    
def found_model(cabin : str, shaft: str):
    print("Found model", cabin, shaft)
    visualizer_scene.load_elevator(cabin, shaft)

def load_manual_building():
    visualizer_scene.load_building("manual.obj")
    manual_editor_scene.disable()
    switch_to_visualizer()
    
# Subscription to events
entry_scene.subscribe_to_move_to_visualizer(switch_to_visualizer)
entry_scene.subscribe_to_elevator(found_model)
entry_scene.subscribe_to_build_building(build_house)
entry_scene.subscribe_to_open_manual_editor(switch_to_manual_editor)
manual_editor_scene.subscribe_to_move_to_visualizer(load_manual_building)
entry_scene.enable()
visualizer_scene.disable()
manual_editor_scene.disable()
app.run()
