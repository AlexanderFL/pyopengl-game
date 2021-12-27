
from game_objects.GameObjectBase import GameObject
from objects.Cube import CubeObject
from shaders.Shaders import Shader3D

import pygame
from OpenGL.GL import *
import sys

class Floor(GameObject):
    """
        The floor gameobject
    """
    def __init__(self, x, y, z, size=20):
        super().__init__(x, y, z)
        self.size = size
        self.cube = CubeObject()
        self.destroy = False

        floor_texture = sys.path[0] + "\\game_objects\\textures\\metal_big_floor-min.png"
        self.texture_id = self.load_texture(floor_texture)
    
    def load_texture(self, path):
        image = pygame.image.load(path)
        tex_string = pygame.image.tostring(image, "RGBA", 1)
        img_width = image.get_width()
        img_height = image.get_height()
        # Start opengl operations
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        # Generate a mipmap for the texture
        glGenerateMipmap(GL_TEXTURE_2D)
        return tex_id

    def collision(self, n) -> None:
        # Skip collision checking
        return None

    def draw(self, modelMatrix, shader:Shader3D, update_shader=False) -> None:
        # Implement the draw call
        modelMatrix.load_identity()
        modelMatrix.push_matrix()

        modelMatrix.add_translation(self.x, self.y, self.z)
        modelMatrix.add_scale(self.size, 0.1, self.size)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        shader.set_material_diffuse(80/255, 123/255, 231/255)
        shader.set_model_matrix(modelMatrix.matrix)
        shader.set_material_shininess(1)
        self.cube.draw(shader)
        modelMatrix.pop_matrix()
    
    def update(self, delta_time, game_objects):
        pass
