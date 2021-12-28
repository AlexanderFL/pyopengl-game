from common_game_maths.Vector import Vector
from .GameObjectBase import GameObject
from .meshes.ObjLoader import load_obj_file
import sys

class Crate(GameObject):
    def __init__(self, x, y, z, scale, rotate=Vector(0, 0, 0)) -> None:
        super().__init__(x, y, z)
        self.scale = scale
        self.rotate = rotate

        obj_file_path = sys.path[0] + "\\models"
        obj_file_name = "crate.obj"
        self.create_obj = load_obj_file(obj_file_path, obj_file_name)
        self.collision_side = [0, 0, 0, 0] # Left x, right x, left z, right z
        self.destroy = False
    
    def update(self, delta_time):
        pass
    
    def collision(self, player_pos) -> GameObject:
        # Implement collision
        self.collision_side = [0, 0, 0, 0]
        p_x = player_pos.x
        p_z = player_pos.z

        x1 = self.x + (self.scale/2 + 0.2)
        x2 = self.x - (self.scale/2 + 0.2)

        z1 = self.z + (self.scale/2 + 0.2)
        z2 = self.z - (self.scale/2 + 0.2)
        
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
            return self
        return None
    
    def draw(self, modelMatrix, shader):
        modelMatrix.push_matrix()
        modelMatrix.load_identity()
        modelMatrix.add_translation(self.x, self.y, self.z)
        modelMatrix.add_rotate_x(self.rotate.x)
        modelMatrix.add_rotate_y(self.rotate.y)
        modelMatrix.add_rotate_z(self.rotate.z)
        modelMatrix.add_scale(self.scale, self.scale, self.scale)
        shader.set_model_matrix(modelMatrix.matrix)
        self.create_obj.draw(shader)
        modelMatrix.pop_matrix()