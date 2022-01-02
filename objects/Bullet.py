import json
from maths.Point import Point
from maths.Vector import Vector
from numpy.lib.function_base import delete
from maths.Color import Color
from objects.primatives.SpherePrimative import SpherePrimative
from .GameObjectBase import GameObject
from maths.Material import Material
from builtins import staticmethod

class Bullet(GameObject):
    def __init__(self, shader, position=Point(1, 1, 1), direction=Vector(1, 0, 0)):
        bullet_material = Material(Color(1, 0, 0), Color(1, 0, 0), 1)
        super().__init__(shader, position, Vector(0,0,0), Vector(0.1, 0.1, 0.1), bullet_material)
        self.direction = direction
        
        self.speed = 10
        self.sphere = SpherePrimative()
        self.collision_resize = 1
    
    def update(self, delta_time, game_objects):
        self.position += self.direction * delta_time * self.speed
        
        if self.position.y <= -1 or self.position.y >= 15:
            self.destroy = True
        if abs(self.position.x) >= 15 or abs(self.position.z) >= 15:
            self.destroy = True
        
        collision_objects = game_objects.check_collision(self)
        
        for obj in collision_objects:
            if type(obj) != Bullet:
                self.destroy = True

    def draw(self, modelMatrix):
        self._draw(modelMatrix, self.sphere)
    
    def serialize(self):
        bullet_dict = {
            'direction':
            {
                'x': self.direction.x,
                'y': self.direction.y,
                'z': self.direction.z
            },
            'position':
            {
                'x': self.position.x,
                'y': self.position.y,
                'z': self.position.z
            }
        }
        return json.dumps(bullet_dict)
    
    @staticmethod
    def deserialize(json_obj):
        bullet_dict = json.loads(json_obj)
        return bullet_dict