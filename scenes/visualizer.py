import json

from ursina import *
from ursina.shaders import lit_with_shadows_shader
import scenes.scene_object
import hacky_test_stuff.fileGeneration

class VisualizerScene(scenes.scene_object.SceneObject):
    def __init__(self):
        super().__init__()

        ## global variables
        self.default_floor_opacity = 0.25
        self.default_floor_color = color.rgba32(16, 128, 255, 255 * self.default_floor_opacity)
        self.suppressed_floor_opacity = 0.02
        self.suppressed_floor_color = color.rgba32(16, 128, 255, 255 * self.suppressed_floor_opacity)

        self.placed_elevator_opacity = 0.95
        self.placed_elevator_color = color.rgba32(224, 76, 76, 255 * self.placed_elevator_opacity)
        self.unplaced_elevator_opacity = 0.1
        self.unplaced_elevator_color = color.rgba32(224, 76, 76, 255 * self.unplaced_elevator_opacity)
        self.elevator_location = None

        self.elevator_indicator_opacity = 0.8
        self.elevator_indicator_color = color.rgba32(255, 0, 0, 255 * self.elevator_indicator_opacity)

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

        self.elevator_parent = Entity()
        self.elevator_parent.parent = self.scene
        self.elevator_parent.enabled = False


        self.is_dragging = False
        self.previous_mouse_position = None
        self.building_parent = None
        self.scene.enabled = False
        self.ui.enabled = False

        self.heightCounter=0

        self.save_button = Button(text='Save', scale=(0.1, 0.05), origin=(0, 0), x=-0.5, y=0.1, color=color.azure)
        self.save_button.tooltip = Tooltip('Save the current state')
        self.save_button.on_click = self.save
        self.save_button.parent = self.ui



    def enable(self):
        self.scene.enabled = True
        self.ui.enabled = True

    def disable(self):
        self.scene.enabled = False
        self.ui.enabled = False

    def save(self):
        data = {
            'input_files': [child.model.name for child in self.building_parent.children if child.model and child.model.name!="sphere"],
            'elevator_position': (self.elevator_parent.world_position[0],self.elevator_parent.world_position[1],self.elevator_parent.world_position[2]) if self.elevator_parent else None
        }
        with open('save_data.json', 'w') as f:
            json.dump(data, f)
        print("State saved to save_data.json")



    def load_building(self, name: str = None):
        floor_array = []
        building_parent = Entity()
        if name:
            if not name=="Default":
                last=name.split("/")[-1]
                fFormat=last.split(".")[-1]

                if not fFormat=="obj":
                    last = hacky_test_stuff.fileGeneration.gatherFileDataFromAndReturnABJ(name, last)

                floor=Entity(model=last, scale=(0.5, 1, 0.5), y=self.heightCounter, collider='box')
                self.heightCounter+=2
                floor.color = self.default_floor_color
                floor.shader = lit_with_shadows_shader
                floor_array.append(floor)
                floor.parent = building_parent

            else:
                for i in range(4):
                    this_floor = Entity(model=f'floor{i}.obj', y=i, collider='box')
                    this_floor.scale = (0.5, 1, 0.5)
                    this_floor.color = self.default_floor_color
                    this_floor.shader = lit_with_shadows_shader
                    floor_array.append(this_floor)
                    this_floor.parent = building_parent
            building_parent.enabled = True


        else:
            for i in range(10):
                this_floor = Entity(model='cube', scale=(10, 1, 10), y=i, collider='box')
                this_floor.color = self.default_floor_color
                this_floor.shader = lit_with_shadows_shader
                floor_array.append(this_floor)
                floor_array.append(this_floor)
                floor_array.append(this_floor)
                this_floor.parent = building_parent

        building_parent.children[0].on_click = self.check_click
        building_parent.parent = self.scene
        self.building_parent = building_parent
        return building_parent



    def load_elevator(self, cabin_: str, shaft_: str,loc:Vec3=Vec3(0,0,0)):
        """This method is called for loading the elevator model"""
        print("Loading elevator", cabin_, shaft_)
        cabin_path = Path(f"models\\{cabin_}")
        shaft_path = Path(f"models\\{shaft_}")
        cabin = Entity(model = load_model("elevator", path=cabin_path))
        shaft = Entity(model = load_model("shaft", path = shaft_path))
        cabin.name = "cabin"
        shaft.name = "shaft"
        self.elevator_location = loc
        cabin.parent = self.elevator_parent
        shaft.parent = self.elevator_parent
        self.elevator_location
        print("models", cabin.model, shaft.model)
        for child in self.elevator_parent.children:
            child.shader = lit_with_shadows_shader
            child.color = color.rgba(0,0,0,0)

        #TODO scale the cabin and shaft to fit the building

    def place_elevator(self):
        self.done_placing_button.enabled = True
        self.elevator_parent.enabled = True
        elevator_indicator = Entity(model="sphere", scale=1, y=1)
        elevator_indicator.parent = self.building_parent
        elevator_indicator.color = self.elevator_indicator_color
        self.elevator_parent.parent = elevator_indicator
        self.placing_elevator = elevator_indicator

        for this_floor in self.building_parent.children[1:]:
            this_floor.animate("color", self.suppressed_floor_color, duration=2, curve=curve.in_out_expo)
            this_floor.collision = False

        self.camera.animate('position', self.building_parent.children[0].position + Vec3(0, 0, 0), duration=2, curve=curve.in_out_expo)
        self.camera.animate('rotation_x', 90, duration=2, curve=curve.in_out_expo)
        self.camera.animate('rotation_y', 0, duration=2, curve=curve.in_out_expo)
        self.camera.animate('rotation_z', 0, duration=2, curve=curve.in_out_expo)
        self.camera.animate('target_z', -30, duration=2, curve=curve.in_out_expo)
        elevator_indicator.animate('color', self.elevator_indicator_color, duration=2, curve=curve.in_out_expo)
        for child in self.elevator_parent.children:
            child.animate("color", self.unplaced_elevator_color, duration=2, curve=curve.in_out_expo)

    def done_placing(self):
        self.done_placing_button.enabled = False
        world_position = self.placing_elevator.world_position
        self.placing_elevator.animate("color", color.rgba32(100, 0, 0, 0.1), duration=2, curve=curve.in_out_expo)


        for this_floor in self.building_parent.children[1:]:
            this_floor.animate("color", self.default_floor_color, duration=2, curve=curve.in_out_expo)
            this_floor.collision = False
        
        # Indicator -> Elevator parent -> Cabin and shaft
        self.elevator_parent.parent = self.scene
        
        for child in self.elevator_parent.children:
            print(child.name)
            child.animate("color", self.placed_elevator_color, duration=2, curve=curve.in_out_expo)
            child.parent = self.elevator_parent
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
        #print(self.camera.target_z)
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