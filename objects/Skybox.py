from os import path
from OpenGL.GL import *
from OpenGL.GLU import projection
from shaders.SkyboxShader import SkyboxShader
import sys
import pygame
import numpy
import copy

from objects.Cube import CubeObject

class Skybox:
    def  __init__(self) -> None:
        self.cube = CubeObject()
        self.destroy = False

        faces = [
            sys.path[0] + "\\game_objects\\textures\\skybox\\right.jpg",
            sys.path[0] + "\\game_objects\\textures\\skybox\\left.jpg",
            sys.path[0] + "\\game_objects\\textures\\skybox\\top.jpg",
            sys.path[0] + "\\game_objects\\textures\\skybox\\bottom.jpg",
            sys.path[0] + "\\game_objects\\textures\\skybox\\front.jpg",
            sys.path[0] + "\\game_objects\\textures\\skybox\\back.jpg"
        ]

        self.cubemapTexture = self.load_cubemap(faces)

        self.texture = sys.path[0] + "\\game_objects\\textures\\skybox\\right.jpg"
        self.texture_id = self.load_texture(self.texture)

        self.shader = SkyboxShader()
        # self.shader.use()
        # self.shader.set_skybox(self.cubemapTexture)
    
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

    def load_cubemap(self, faces):
        textureId = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureId)

        counter = 0
        for img_path in faces:
            image_data = pygame.image.load(img_path)
            image_tex_string = pygame.image.tostring(image_data, "RGBA", 1)
            image_width = image_data.get_width()
            image_height = image_data.get_height()
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + counter, 0, GL_RGB, image_width, image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_tex_string)
            counter += 1
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

        return textureId
    
    def collision(self, player_pos):
        pass

    def update(self, delta_time, game_objects):
        pass
    
    def draw(self, modelMatrix, shader, update_shader=False):
        modelMatrix.load_identity()
        modelMatrix.push_matrix()

        modelMatrix.add_translation(0, 0, 0)
        modelMatrix.add_scale(20, 20, 20)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # shader.set_diffuse_texture(0)
        shader.set_model_matrix(modelMatrix.matrix)
        #shader.set_material_diffuse(1, 1, 1) # TEMPORARY
        #shader.set_material_specular(0.6282, 0.5558, 0.3660)
        # shader.set_material_shininess(100)

        self.cube.draw(shader, update_shader)
        modelMatrix.pop_matrix()
