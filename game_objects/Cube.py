from OpenGL.GL import *
from maths.Matricies import ModelMatrix
from maths.Vector import Vector
from objects.Cube import CubeObject
from game_objects.GameObjectBase import GameObject
from common_game_maths.Point import Point
from math import sqrt, pow
import pygame
import sys

class Cube(GameObject):
    """
        A single cube gameobject that has collision
    """
    def __init__(self, x, y, z, size=(1, 1, 1), color=(0.9, 0.9, 0.9), visible=True, texture_path=None):
        super().__init__(x, y, z)
        self.position = Point(x, y, z)
        self.size_x = size[0]
        self.size_y = size[1]
        self.size_z = size[2]
        self.color = color
        self.cube = CubeObject()
        # x left, x right, z left, z right
        self.moving = [False, False, False, False]
        self.rotation = Vector(0, 0, 0)
        self.visible = visible
        self.position_center = Point(x+self.size_x/2, y+self.size_y/2, z+self.size_z/2)
        self.collision_side = [0, 0, 0, 0] # Left x, right x, left z, right z

        self.destroy = False

        self.apply_texture = sys.path[0] + "\\game_objects\\textures\\missing.png"
        if texture_path != None:
            self.apply_texture = texture_path
        self.texture_id = self.load_texture(self.apply_texture)
    
    def load_texture(self, path):
        image = pygame.image.load(path)
        tex_string = pygame.image.tostring(image, "RGBA", 1)
        img_width = image.get_width()
        img_height = image.get_height()
        # Start opengl operations
        tex_id = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        # Generate a mipmap for the texture
        glGenerateMipmap(GL_TEXTURE_2D)
        return tex_id

    def move(self, change):
        # Change cube position by change
        if self.moving[0]:
            self.x -= change
        if self.moving[1]:
            self.x += change
        if self.moving[2]:
            self.z += change
        if self.moving[3]:
            self.z -= change
        
    def rotate(self, x, y, z) -> None:
        # Rotate the cube by x y z
        self.rotation += Vector(x, y, z)
    
    def collision(self, player_pos) -> GameObject:
        # Implement collision
        self.collision_side = [0, 0, 0, 0]
        p_x = player_pos.x
        p_z = player_pos.z

        x1 = self.x + (self.size_x/2 + 0.2)
        x2 = self.x - (self.size_x/2 + 0.2)

        z1 = self.z + (self.size_z/2 + 0.2)
        z2 = self.z - (self.size_z/2 + 0.2)
        
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
    
    def draw(self, modelMatrix : ModelMatrix, shader, update_shader=False) -> None:
        # Implement the draw call
        if self.visible:
            modelMatrix.load_identity()
            modelMatrix.push_matrix()

            modelMatrix.add_translation(self.x, self.y, self.z)
            modelMatrix.add_rotate_x(self.rotation.x)
            modelMatrix.add_rotate_y(self.rotation.y)
            modelMatrix.add_rotate_z(self.rotation.z)
            modelMatrix.add_scale(self.size_x, self.size_y, self.size_z)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            shader.set_diffuse_texture(0)
            shader.set_model_matrix(modelMatrix.matrix)
            # shader.set_material_diffuse(self.color[0], self.color[1], self.color[2])
            shader.set_material_diffuse(1, 1, 1) # TEMPORARY
            shader.set_material_specular(0.6282, 0.5558, 0.3660)
            shader.set_material_shininess(100)
            
            self.cube.draw(shader, update_shader)
            modelMatrix.pop_matrix()

    def update(self, delta_time, game_objects):
        pass