from ursina import *
from ursina.shaders import lit_with_shadows_shader

import scenes.scene_object

class VisualizerScene(scenes.scene_object.SceneObject):
    def __init__(self):
        super().__init__()
        self.scene = Entity(scale=(1, 1, 1))
        # Create a separate entity for UI elements
        self.ui = Entity(parent=camera.ui)

        self.spin_button = Button(text='Spin', scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.4, color=color.azure)
        self.spin_button.tooltip = Tooltip('Spin the building')
        self.spin_button.on_click = self.spin_building
        self.spin_button.parent = self.ui
        
        self.place_button = Button(text='Place Elevator', scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.3, color=color.azure)
        self.place_button.tooltip = Tooltip('Place an elevator')
        self.place_button.on_click = self.place_elevator_call
        self.place_button.parent = self.ui
        
        self.done_placing_button = Button(text='Done Placing', scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.2, color=color.azure)
        self.done_placing_button.tooltip = Tooltip('Done placing the elevator')
        self.done_placing_button.on_click = self.done_placing
        self.done_placing_button.parent = self.ui
        self.done_placing_button.enabled = False
        
        self.placing_elevator = False
        self.camera = EditorCamera()  # add camera controls for orbiting and moving the camera
        self.camera.parent = self.scene
        
        self.is_dragging = False
        self.previous_mouse_position = None
        self.building_parent = self.load_building()
        self.building_parent.parent = self.scene
        self.building_parent.children[0].on_click = self.check_click
        self.scene.enabled = False
        self.ui.enabled = False

    def enable(self):   
        self.scene.enabled = True
        self.ui.enabled = True

    def disable(self):
        self.scene.enabled = False
        self.ui.enabled = False

    def load_building(self, name: str = None):
        if name:
            Exception("Not implemented")
        else:
            floor_array = []
            building_parent = Entity()
            for i in range(10):
                this_floor = Entity(model='cube', scale=(10, 1, 10), y=i, collider='box')
                this_floor.color = color.rgba32(16, 128, 255, 255 * 0.4)
                this_floor.shader = lit_with_shadows_shader
                floor_array.append(this_floor)
                this_floor.parent = building_parent
            return building_parent

    def place_elevator(self):
        self.done_placing_button.enabled = True
        elevator = Entity(model='cube', scale=(2, 10, 2), y=5)
        elevator.color = color.rgba32(0, 0, 0, 0)
        elevator.shader = lit_with_shadows_shader
        elevator_indicator = Entity(model="sphere", scale=1, y=1)
        elevator_indicator.parent = self.building_parent
        elevator_indicator.color = color.rgba32(255, 0, 0, 0)
        elevator.parent = elevator_indicator
        self.placing_elevator = elevator_indicator

        for this_floor in self.building_parent.children[1:]:
            this_floor.animate("color", color.rgba32(16, 128, 255, 255 * 0.02), duration=2, curve=curve.in_out_expo)
            this_floor.collision = False

        self.camera.animate('position', self.building_parent.children[0].position + Vec3(0, 0, 0), duration=2, curve=curve.in_out_expo)
        self.camera.animate('rotation_x', 90, duration=2, curve=curve.in_out_expo)
        self.camera.animate('rotation_y', 0, duration=2, curve=curve.in_out_expo)
        self.camera.animate('rotation_z', 0, duration=2, curve=curve.in_out_expo)
        self.camera.animate('target_z', -30, duration=2, curve=curve.in_out_expo)
        elevator_indicator.animate('color', color.rgba32(255, 0, 0, 255), duration=2, curve=curve.in_out_expo)
        elevator.animate("color", color.rgba32(224, 76, 76, 255 * 0.1), duration=2, curve=curve.in_out_expo)

    def done_placing(self):
        self.done_placing_button.enabled = False
        world_position = self.placing_elevator.world_position
        self.placing_elevator.animate("color", color.rgba32(0, 0, 0, 0), duration=2, curve=curve.in_out_expo)
        
        for child in self.placing_elevator.children:
            child.animate("color", color.rgba32(224, 76, 76, 255), duration=2, curve=curve.in_out_expo)
            child.parent = self.building_parent
            child.world_position = world_position + child.position
        invoke(self.disable_indicator, delay=2)
        
    def spin(self, e: Entity):
        e.animate('rotation_y', e.rotation_y + 360, duration=2, curve=curve.in_out_expo)

    def spin_building(self):
        self.spin(self.building_parent)

    def place_elevator_call(self):
        self.place_elevator()

    def disable_indicator(self):
        self.placing_elevator.enabled = False
    
    def check_click(self):
        print("Mouse clicked")
        if self.placing_elevator:
            print("Placing elevator")
            self.placing_elevator.animate("position", mouse.world_point, duration=0.5, curve=curve.in_out_expo)

    def update(self):
        print(self.camera.target_z)
        if held_keys['right mouse']:  # Check if right mouse button is held down
            if not self.is_dragging:
                self.is_dragging = True
                self.previous_mouse_position = mouse.position
            else:
                # Calculate the difference in mouse position
                delta = mouse.position - self.previous_mouse_position
                # Adjust camera's rotation based on mouse movement
                self.camera.rotation_y += delta.x * 100  # Adjust rotation sensitivity as needed
                self.camera.rotation_x -= delta.y * 100  # Adjust for up/down movement
                self.previous_mouse_position = mouse.position
        else:
            self.is_dragging = False