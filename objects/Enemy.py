from pygame import Vector3
from objects.GameObjectBase import GameObject
from maths.Point import Point
from maths.Vector import Vector
from .meshes.ObjLoader import load_obj_file
import sys

class Enemy(GameObject):
    def __init__(self, shader, x, y, z, rotate=Vector(0, 0, 0)) -> None:
        super().__init__(x, y, z)
        self.shader = shader
        self.scale = 1
        self.rotate = rotate
        self.collision_side = [0, 0, 0, 0]
        self.colliding = False

        obj_location = sys.path[0] + "\\models\\"
        filename = "bean.obj"
        self.model = load_obj_file(obj_location, filename)
        self.destroy = False
    
    def shoot_bullet(self, bullet_obj):
        pass
    
    def update(self, delta_time, game_objects) -> None:
        self.rotate.y += delta_time

        if self.colliding == True:
            pass
            # self.destroy = True

        self.colliding = False
    
    def collision(self, player_pos) -> GameObject:
        # Implement collision
        self.collision_side = [0, 0, 0, 0]
        p_x = player_pos.x
        p_z = player_pos.z

        x1 = self.x + (self.scale/6 + 0.2)
        x2 = self.x - (self.scale/6 + 0.2)

        z1 = self.z + (self.scale/6 + 0.2)
        z2 = self.z - (self.scale/6 + 0.2)

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
    
    def draw(self, modelMatrix, shader, update_shader=False) -> GameObject:
        # Implement the draw call
        modelMatrix.push_matrix()
        modelMatrix.load_identity()
        modelMatrix.add_translation(self.x, self.y, self.z)
        modelMatrix.add_scale(self.scale, self.scale, self.scale)
        modelMatrix.add_rotate_x(self.rotate.x)
        modelMatrix.add_rotate_y(self.rotate.y)
        modelMatrix.add_rotate_z(self.rotate.z)
        shader.set_model_matrix(modelMatrix.matrix)
        self.model.draw(shader)
        modelMatrix.pop_matrix()