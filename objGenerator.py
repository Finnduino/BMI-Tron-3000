from inference_sdk import InferenceHTTPClient
import json
from shapely.geometry import Polygon as ShapePolygon
import trimesh
import math
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="y6qYqZznWJka0MAyj7Og"
)


def get_predictions(image_path):
    result = CLIENT.infer(image_path, model_id="room-segment-3zyl5/1")
    return result


def create_model(path_of_image: str):
    results = get_predictions(path_of_image)
    #Filter with confidence of 0.1
    culled_results = []
    for result in results["predictions"]:
        if result['confidence'] > 0.1:
            if result['class'] == "floor":
                twoD_points = []
                for point in result["points"]:
                    twoD_points.append([point["x"], point["y"]])
                polygon = ShapePolygon(twoD_points)
                mesh = trimesh.creation.extrude_polygon(polygon, 3.05*30)
                culled_results.append(mesh)
    
    done_mesh = trimesh.util.concatenate(culled_results)
    angle = math.pi / 2
    direction = [1, 0, 0]
    center = [0, 0, 0]
    rotat = trimesh.transformations.rotation_matrix(angle, direction, center)
    done_mesh.apply_transform(rotat)

    scale = trimesh.transformations.scale_matrix(1/30)
    done_mesh.apply_transform(scale)
    done_mesh.export("calculated.obj")
    
    print(results)
    
create_model("hacky_test_aleksis\\input_image.png")