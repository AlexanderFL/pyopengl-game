import json
from pygame import Vector3
from objects.GameObjectBase import GameObject
from maths.Point import Point
from maths.Vector import Vector
from objects.Player import Player
from .meshes.ObjLoader import load_obj_file
import sys

class Enemy(GameObject):
    def __init__(self, shader, position, rotation, scale, material, visible=True) -> None:
        super().__init__(shader, position, rotation, scale, material, visible)
        self.collision_resize = 6

        obj_location = sys.path[0] + "\\models\\"
        filename = "bean.obj"
        self.model = load_obj_file(obj_location, filename)
        self.network_uid = None
    
    def shoot_bullet(self, bullet_obj):
        pass
    
    def update(self, delta_time, game_objects) -> None:
        pass
        # self.rotation.y += delta_time

        # WIP
        #collision_objects = game_objects.check_collision(Point(self.x, self.y, self.z))
        #print(collision_objects)
    
    def draw(self, modelMatrix) -> GameObject:
        self._draw(modelMatrix, self.model)
    
    def deserialize(self, p_json):
        p_dict = json.loads(p_json)
        position = p_dict["position"]
        visible = not p_dict["dead"]
        
        self.position = Vector(position["x"], position["y"], position["z"])
        self.visible = visible