from ursina import *
import scenes.scene_object
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser import FileButton
from ursina.prefabs.input_field import InputField
import tkinter as tk
from tkinter import filedialog
import PIL
from ursina.shaders import basic_lighting_shader
import trimesh
from shapely.geometry import Polygon as ShapePolygon
class ManualEditor(scenes.scene_object.SceneObject):
    def __init__(self):
        super().__init__()
        
        self.move_to_visualizer_callback = None
        
        self.initial_setup = Entity(parent=self.ui, origin=(0, 0), position=(0, 0))
        self.autofill_title = Text("Select the base drawing", position=(0, 0.3), origin=(0, 0))
        self.autofill_title.parent = self.initial_setup
        self.select_button = Button(text='Browse File', color=color.azure, y=0.2, origin=(0, 0))
        self.select_button.fit_to_text()
        self.select_button.tooltip = Tooltip('Select the base drawing to start editing')
        self.select_button.on_click = self.open_image_dialog
        self.select_button.parent = self.initial_setup
        
        
        self.active = Entity(parent=self.ui, origin=(0, 0), position=(-0.5, 0))
        self.active.enabled = False
        self.active_title = Text("Click on the walls to build the layout", position=(0, 0.3), origin=(0, 0))
        self.active_title.parent = self.active
        
        self.base_image = None
        self.camera = EditorCamera()
        self.camera.orthographic = True
        self.camera.parent = self.scene
        
        done_button = Button(text='Done', color=color.azure, y=0.2, origin=(0, 0))
        done_button.fit_to_text()
        done_button.tooltip = Tooltip('Finish drawing the layout')
        done_button.on_click = self.done_drawing
        done_button.parent = self.active
        
        self.building_polygon = False
        self.position_collection = []
        self.indicator_parent = Entity( parent=self.scene)
        self.indicator_line = Entity(parent=self.indicator_parent)
        
    def open_image_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Image files", ["*.png" ,"*.jpg", " *.jpeg"])])
        #move the file to the correct location
        
        self.initialize_image(file_path)
        
    def initialize_image(self, file_path):
        pil_image = PIL.Image.open(file_path)
        aspect_ratio = pil_image.width / pil_image.height
        print(aspect_ratio)
        self.base_image = Entity(model=Plane((2,2)), collider = "box", scale=(aspect_ratio,1,1)*29, position=(0, 0, -2), origin=(0,0,0), color=color.rgba(255, 255, 255, 255))        
        self.camera.animate("rotation_x", 90, duration=0, curve=curve.linear)
        self.camera.animate("position", (0, 1, 0), duration=0, curve=curve.linear)
        self.base_image.texture = Texture(pil_image)
        self.base_image.parent = self.scene
        self.initial_setup.enabled = False
        self.scene.enabled = True
        self.ui.enabled = True
        self.active.enabled = True
        self.building_polygon = True
        self.base_image.on_click = self.check_click
    
    def check_click(self):
        print("Clicked on the image")
        if self.building_polygon:
            
            self.place_indicator(mouse.world_point)
            
            
    def place_indicator(self, position):
        indicator = Entity(model="Sphere", scale=1, position=position, color=color.red)
        indicator.parent = self.indicator_parent
        self.position_collection.append(position)
        if len(self.position_collection) > 1:
            self.indicator_line.shader = basic_lighting_shader
            self.indicator_line.color = color.rgba(255, 0, 0, 190)
            loop = self.position_collection + [self.position_collection[0]]
            self.indicator_line.model = Pipe(path=loop, thickness=1, base_shape=Cube(subdivisions=(3,3,3)))	

    def done_drawing(self):
        loop = self.position_collection + [self.position_collection[0]]
        self.construct_floor(loop)
        
        
    def construct_floor(self, loop, height=1):
        #flatten loop
        for i in range(len(loop)):
            loop[i] = [loop[i].x, loop[i].z]
        polygon = ShapePolygon(loop)
        mesh = trimesh.creation.extrude_polygon(polygon, height)
        mesh.export("demo.obj")
        self.move_to_visualizer_callback()
    
    def subscribe_to_move_to_visualizer(self, methodname):
        self.move_to_visualizer_callback = methodname