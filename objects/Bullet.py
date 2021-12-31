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
        self.scale = 1

        self.destroy = False
    
    def collision(self, player_pos):
        self.collision_side = [0, 0, 0, 0]
        p_x = player_pos.x
        p_z = player_pos.z

        x1 = self.position.x + (self.scale/6 + 0.2)
        x2 = self.position.x - (self.scale/6 + 0.2)

        z1 = self.position.z + (self.scale/6 + 0.2)
        z2 = self.position.z - (self.scale/6 + 0.2)

        if p_x <= x1 and p_x >= x2 and p_z <= z1 and p_z >= z2:
            x_h1 = abs(p_x - x1)
            x_h2 = abs(p_x - x2)
            z_h1 = abs(p_z - z1)
            z_h2 = abs(p_z - z2)

            if x_h1 < x_h2 and x_h1 < z_h1 and x_h1 < z_h2:
                self.collision_side[0] = 1
            elif x_h2 < x_h1 and x_h2 < z_h1 and x_h2 < z_h2:
                self.collision_side[1] = 1
            elif z_h1 < x_h1 and z_h1 < x_h2 and z_h1 < z_h2:
                self.collision_side[2] = 1
            elif z_h2 < x_h1 and z_h2 < x_h2 and z_h2 < z_h1:
                self.collision_side[3] = 1
            self.colliding = True
            return self
        return None
    
    def update(self, delta_time, game_objects):
        self.position += self.direction * delta_time * self.speed
        
        if self.position.y <= -1 or self.position.y >= 15:
            self.destroy = True
        if abs(self.position.x) >= 15 or abs(self.position.z) >= 15:
            self.destroy = True
        
        collision_objects = game_objects.check_collision(self.position)
        
        for obj in collision_objects:
            if type(obj) != Bullet:
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