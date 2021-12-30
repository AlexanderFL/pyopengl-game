import json
from common_game_maths.Point import Point
from common_game_maths.Vector import Vector
from numpy.lib.function_base import delete
from objects.primatives.SpherePrimative import SpherePrimative

class Bullet:
    def __init__(self, shader, position=Point(1, 1, 1), direction=Vector(1, 0, 0)):
        self.shader = shader
        self.position = position
        self.direction = direction
        self.speed = 10

        self.size_x = 0.1
        self.size_y = 0.1
        self.size_z = 0.1

        self.color = (1, 0.0, 0.0)
        self.sphere = SpherePrimative()

        self.destroy = False
    
    def collision(self, player_pos):
        pass
    
    def update(self, delta_time, game_objects):
        self.position += self.direction * delta_time * self.speed
        
        if self.position.y <= -1 or self.position.y >= 15:
            self.destroy = True
        if abs(self.position.x) >= 15 or abs(self.position.z) >= 15:
            self.destroy = True
        
        collision_objects = game_objects.check_collision(self.position)

        if collision_objects != []:
            self.destroy = True

    def draw(self, modelMatrix, shader, update_shader=False):
        modelMatrix.load_identity()
        modelMatrix.push_matrix()

        modelMatrix.add_translation(self.position.x, self.position.y, self.position.z)
        modelMatrix.add_scale(self.size_x, self.size_y, self.size_z)

        shader.set_model_matrix(modelMatrix.matrix)
        shader.set_material_diffuse(self.color[0], self.color[1], self.color[2])
        shader.set_material_specular(self.color[0], self.color[1], self.color[2])
        self.sphere.draw(self.shader)
        modelMatrix.pop_matrix()
    
    def get_dict(self):
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
        return bullet_dict